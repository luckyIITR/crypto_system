"""
Market order placement functionality.

This module provides functions to place market orders on Delta Exchange.
"""

from __future__ import annotations

from typing import Any, Optional

from config import get_client


def place_market_order(
    *,
    product_id: Optional[int] = None,
    product_symbol: Optional[str] = None,
    size: int,
    side: str,
    stop_order_type: Optional[str] = None,
    stop_price: Optional[str] = None,
    trail_amount: Optional[str] = None,
    stop_trigger_method: Optional[str] = None,
    bracket_stop_trigger_method: Optional[str] = None,
    bracket_stop_loss_limit_price: Optional[str] = None,
    bracket_stop_loss_price: Optional[str] = None,
    bracket_trail_amount: Optional[str] = None,
    bracket_take_profit_limit_price: Optional[str] = None,
    bracket_take_profit_price: Optional[str] = None,
    time_in_force: Optional[str] = None,
    mmp: Optional[str] = None,
    post_only: Optional[str] = None,
    reduce_only: Optional[str] = None,
    client_order_id: Optional[str] = None,
    cancel_orders_accepted: Optional[str] = None,
) -> dict[str, Any]:
    """
    Place a market order on Delta Exchange.

    A market order is executed immediately at the current market price.
    For market orders, limit_price is not required.

    Parameters
    ----------
    product_id : int, optional
        Product ID. Only one of either product_id or product_symbol must be sent.
    product_symbol : str, optional
        Product symbol (e.g., 'BTCUSD'). Only one of either product_id or
        product_symbol must be sent.
    size : int
        Order size (required).
    side : str
        Order side: 'buy' or 'sell' (required).
    stop_order_type : str, optional
        Stop order type: 'stop_loss' or 'take_profit'.
    stop_price : str, optional
        Stop loss price level if the order is a stop order.
    trail_amount : str, optional
        Trail amount if you want a trailing stop order. Required if stop_price
        is empty.
    stop_trigger_method : str, optional
        Stop order trigger method: 'mark_price', 'last_traded_price', or
        'spot_price'.
    bracket_stop_trigger_method : str, optional
        Stop order trigger method for bracket orders: 'mark_price',
        'last_traded_price', or 'spot_price'.
    bracket_stop_loss_limit_price : str, optional
        Bracket order stop loss limit price.
    bracket_stop_loss_price : str, optional
        Bracket order stop loss trigger price.
    bracket_trail_amount : str, optional
        Bracket trail amount if you want a trailing stop order. Required if
        bracket stop price is empty.
    bracket_take_profit_limit_price : str, optional
        Bracket order take profit limit price.
    bracket_take_profit_price : str, optional
        Take profit trigger price for bracket order.
    time_in_force : str, optional
        Order type: 'GTC' (Good Till Cancel) or 'IOC' (Immediate Or Cancel).
    mmp : str, optional
        MMP level for the order: 'disabled', 'mmp1', 'mmp2', 'mmp3', 'mmp4', 'mmp5'.
    post_only : str, optional
        Post only order flag.
    reduce_only : str, optional
        If set, will only close positions. New orders will not be placed.
    client_order_id : str, optional
        Custom ID provided by user when creating order (max 32 length).
    cancel_orders_accepted : str, optional
        If set, will cancel all existing orders for the product.

    Returns
    -------
    dict[str, Any]
        API response containing the order details.

    Raises
    ------
    ValueError
        If neither product_id nor product_symbol is provided, or if both are
        provided, or if required parameters are missing.

    Examples
    --------
    >>> # Simple market buy order
    >>> response = place_market_order(
    ...     product_symbol="BTCUSD",
    ...     size=1,
    ...     side="buy"
    ... )
    >>>
    >>> # Market sell order with reduce_only
    >>> response = place_market_order(
    ...     product_id=27,
    ...     size=2,
    ...     side="sell",
    ...     reduce_only="true"
    ... )
    """
    # Validate that exactly one of product_id or product_symbol is provided
    if product_id is None and product_symbol is None:
        raise ValueError(
            "Either product_id or product_symbol must be provided (but not both)."
        )

    if product_id is not None and product_symbol is not None:
        raise ValueError(
            "Only one of product_id or product_symbol should be provided, not both."
        )

    # Validate required parameters
    if size is None:
        raise ValueError("size is required.")

    if not side or side.lower() not in ("buy", "sell"):
        raise ValueError("side must be either 'buy' or 'sell'.")

    # Build order parameters
    order_params: dict[str, Any] = {
        "order_type": "market_order",
        "size": size,
        "side": side.lower(),
    }

    # Add product identifier
    if product_id is not None:
        order_params["product_id"] = product_id
    if product_symbol is not None:
        order_params["product_symbol"] = product_symbol

    # Add optional parameters if provided
    if stop_order_type is not None:
        order_params["stop_order_type"] = stop_order_type
    if stop_price is not None:
        order_params["stop_price"] = stop_price
    if trail_amount is not None:
        order_params["trail_amount"] = trail_amount
    if stop_trigger_method is not None:
        order_params["stop_trigger_method"] = stop_trigger_method
    if bracket_stop_trigger_method is not None:
        order_params["bracket_stop_trigger_method"] = bracket_stop_trigger_method
    if bracket_stop_loss_limit_price is not None:
        order_params["bracket_stop_loss_limit_price"] = bracket_stop_loss_limit_price
    if bracket_stop_loss_price is not None:
        order_params["bracket_stop_loss_price"] = bracket_stop_loss_price
    if bracket_trail_amount is not None:
        order_params["bracket_trail_amount"] = bracket_trail_amount
    if bracket_take_profit_limit_price is not None:
        order_params["bracket_take_profit_limit_price"] = bracket_take_profit_limit_price
    if bracket_take_profit_price is not None:
        order_params["bracket_take_profit_price"] = bracket_take_profit_price
    if time_in_force is not None:
        order_params["time_in_force"] = time_in_force
    if mmp is not None:
        order_params["mmp"] = mmp
    if post_only is not None:
        order_params["post_only"] = post_only
    if reduce_only is not None:
        order_params["reduce_only"] = reduce_only
    if client_order_id is not None:
        if len(client_order_id) > 32:
            raise ValueError("client_order_id must be 32 characters or less.")
        order_params["client_order_id"] = client_order_id
    if cancel_orders_accepted is not None:
        order_params["cancel_orders_accepted"] = cancel_orders_accepted

    # Get client and place order
    client = get_client()
    response = client.place_order(**order_params)

    return response

