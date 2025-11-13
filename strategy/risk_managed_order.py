"""
Risk-managed market order placement with automatic stop loss calculation.

This module provides methods to place market orders with stop loss levels
calculated from recent candle data and position sizing based on risk management.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Optional

import pandas as pd

from config import get_client
from data import get_historical_candles
from order_management import place_market_order
from strategy.lot_sizes import get_lot_size, convert_to_lots


def place_risk_managed_market_order(
    *,
    side: str,
    product_id: Optional[int] = None,
    product_symbol: Optional[str] = None,
    risk_per_trade: float,
    timeframe: str = "5m",
    candles_count: int = 5,
    **additional_params: Any,
) -> dict[str, Any]:
    """
    Place a market order with automatic stop loss based on recent candle data.

    The stop loss is calculated from the last N candles:
    - For SELL orders: SL = highest high of last N candles
    - For BUY orders: SL = lowest low of last N candles

    Position size is calculated as: risk_per_trade / sl_points
    where sl_points = |current_market_price - stop_loss_price|

    Parameters
    ----------
    side : str
        Order side: 'buy' or 'sell' (case-insensitive).
    product_id : int, optional
        Product ID. Only one of product_id or product_symbol must be provided.
    product_symbol : str, optional
        Product symbol (e.g., 'BTCUSD'). Only one of product_id or product_symbol
        must be provided.
    risk_per_trade : float
        Risk amount per trade (in base currency). This is the maximum amount
        you're willing to lose on this trade.
    timeframe : str, default '5m'
        Timeframe for candles used to calculate stop loss (e.g., '5m', '15m', '1h').
    candles_count : int, default 5
        Number of recent candles to use for stop loss calculation.
    **additional_params : Any
        Additional parameters to pass to the market order (e.g., reduce_only,
        time_in_force, etc.).

    Returns
    -------
    dict[str, Any]
        API response containing the order details, including:
        - market_order: The placed market order details (includes stop loss via bracket)
        - stop_loss_order: None (stop loss is included in the market order as bracket_stop_loss_price)
        - calculated_values: Dictionary with calculated SL price, SL points,
          position size, etc.

    Raises
    ------
    ValueError
        If parameters are invalid or insufficient data is available.
    Exception
        If order placement fails.

    Examples
    --------
    >>> # Place a BUY order with $100 risk
    >>> response = place_risk_managed_market_order(
    ...     side="buy",
    ...     product_symbol="BTCUSD",
    ...     risk_per_trade=100.0
    ... )
    >>>
    >>> # Place a SELL order with custom timeframe
    >>> response = place_risk_managed_market_order(
    ...     side="sell",
    ...     product_id=27,
    ...     risk_per_trade=50.0,
    ...     timeframe="15m",
    ...     candles_count=10
    ... )
    """
    # Validate side
    side_lower = side.lower()
    if side_lower not in ("buy", "sell"):
        raise ValueError("side must be either 'buy' or 'sell'")

    # Validate product identifier
    if product_id is None and product_symbol is None:
        raise ValueError(
            "Either product_id or product_symbol must be provided."
        )

    if product_id is not None and product_symbol is not None:
        raise ValueError(
            "Only one of product_id or product_symbol should be provided."
        )

    # Validate risk_per_trade
    if risk_per_trade <= 0:
        raise ValueError("risk_per_trade must be greater than 0")

    # Get client to fetch current market price
    client = get_client()

    # Determine product identifier for API calls
    product_identifier = {"product_id": product_id} if product_id else {"product_symbol": product_symbol}

    # For historical candles, we need a symbol (string)
    # If only product_id is provided, we'll need to use it as symbol (may need adjustment)
    candle_symbol = product_symbol if product_symbol else str(product_id)

    # Get recent candles for stop loss calculation
    print(f"Fetching last {candles_count} candles of {timeframe} timeframe...")
    end_time = datetime.now()
    # Fetch more candles than needed to ensure we have enough data
    start_time = end_time - timedelta(days=1)

    try:
        candles_df = get_historical_candles(
            resolution=timeframe,
            symbol=candle_symbol,
            start=start_time,
            end=end_time,
        )
    except Exception as e:
        raise ValueError(
            f"Failed to fetch historical candles: {e}. "
            "Please check if product_symbol or product_id is valid."
        ) from e

    if len(candles_df) < candles_count:
        raise ValueError(
            f"Insufficient candle data. Found {len(candles_df)} candles, "
            f"but need at least {candles_count} candles."
        )

    # Get last N candles
    last_candles = candles_df.tail(candles_count)

    # Calculate stop loss based on side
    if side_lower == "sell":
        # For SELL: SL = highest high of last N candles
        stop_loss_price = float(last_candles["high"].max())
    else:  # buy
        # For BUY: SL = lowest low of last N candles
        stop_loss_price = float(last_candles["low"].min())

    # Get current market price (use latest close price)
    current_price = float(candles_df["close"].iloc[-1])

    # Calculate SL points
    sl_points = abs(current_price - stop_loss_price)
    if sl_points == 0:
        raise ValueError(
            "Stop loss price equals current market price. "
            "Cannot calculate position size."
        )

    # Get lot size for the product
    lot_size = get_lot_size(product_symbol=product_symbol)
    
    # Calculate position size in base currency: risk_per_trade / sl_points
    position_size_base = risk_per_trade / sl_points
    
    # Convert to lots
    position_size_lots = convert_to_lots(position_size_base, lot_size)

    if position_size_lots <= 0:
        raise ValueError(
            f"Calculated position size is {position_size_lots} lots (must be > 0). "
            f"This may happen if risk_per_trade ({risk_per_trade}) is too small "
            f"relative to SL points ({sl_points:.2f}). "
            f"Lot size for this product: {lot_size}."
        )
    
    # Position size for API is in lots
    position_size = position_size_lots

    # Calculate actual position size in base currency for display
    from strategy.lot_sizes import convert_from_lots
    position_size_base_currency = convert_from_lots(position_size, lot_size)
    
    print(f"\nCalculated Values:")
    print(f"  Current Price: {current_price:.2f}")
    print(f"  Stop Loss Price: {stop_loss_price:.2f}")
    print(f"  SL Points: {sl_points:.2f}")
    print(f"  Risk per Trade: {risk_per_trade:.2f}")
    print(f"  Lot Size: {lot_size}")
    print(f"  Position Size: {position_size} lots ({position_size_base_currency:.6f} base currency)")

    # Place market order with bracket stop loss
    print(f"\nPlacing {side_lower.upper()} market order with stop loss at {stop_loss_price:.2f}...")
    market_order_params = {
        **product_identifier,
        "size": position_size,
        "side": side_lower,
        "bracket_stop_loss_price": str(stop_loss_price),
        "bracket_stop_trigger_method": "last_traded_price",
        **additional_params,
    }

    try:
        market_order_response = place_market_order(**market_order_params)
    except Exception as e:
        raise Exception(f"Failed to place market order: {e}") from e

    # Stop loss is included in the market order, no separate order needed
    stop_order_response = None

    # Prepare response
    # Note: stop_loss_order is None since stop loss is included in the market order
    response: dict[str, Any] = {
        "success": True,
        "market_order": market_order_response,
        "stop_loss_order": stop_order_response,  # None - stop loss included in market order
        "calculated_values": {
            "current_price": current_price,
            "stop_loss_price": stop_loss_price,
            "sl_points": sl_points,
            "risk_per_trade": risk_per_trade,
            "position_size": position_size,
            "position_size_base_currency": position_size_base_currency,
            "lot_size": lot_size,
            "timeframe": timeframe,
            "candles_count": candles_count,
            "side": side_lower,
        },
    }

    return response

