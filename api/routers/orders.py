"""
Order management API endpoints.

This router handles BUY and SELL order placement with risk management.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, model_validator

from strategy import place_risk_managed_market_order

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


class RiskManagedOrderRequest(BaseModel):
    """Request model for risk-managed market orders."""

    product_id: int | None = Field(
        None,
        description="Product ID. Only one of product_id or product_symbol must be provided.",
    )
    product_symbol: str | None = Field(
        None,
        description="Product symbol (e.g., 'BTCUSD'). Only one of product_id or product_symbol must be provided.",
    )
    risk_per_trade: float = Field(
        ...,
        gt=0,
        description="Risk amount per trade (in base currency). Maximum amount willing to lose on this trade.",
    )
    timeframe: str = Field(
        default="5m",
        description="Timeframe for candles used to calculate stop loss (e.g., '5m', '15m', '1h').",
    )
    candles_count: int = Field(
        default=5,
        ge=1,
        le=100,
        description="Number of recent candles to use for stop loss calculation.",
    )
    reduce_only: str | None = Field(
        None,
        description="If set, will only close positions. New orders will not be placed.",
    )
    time_in_force: str | None = Field(
        None,
        description="Order type: 'GTC' (Good Till Cancel) or 'IOC' (Immediate Or Cancel).",
    )
    client_order_id: str | None = Field(
        None,
        max_length=32,
        description="Custom ID provided by user when creating order (max 32 length).",
    )

    @model_validator(mode="after")
    def validate_product_identifier(self) -> "RiskManagedOrderRequest":
        """Ensure exactly one of product_id or product_symbol is provided."""
        if self.product_id is None and self.product_symbol is None:
            raise ValueError("Either product_id or product_symbol must be provided.")
        if self.product_id is not None and self.product_symbol is not None:
            raise ValueError(
                "Only one of product_id or product_symbol should be provided, not both."
            )
        return self


class OrderResponse(BaseModel):
    """Response model for order placement."""

    success: bool
    message: str
    market_order: dict[str, Any] | None = None
    stop_loss_order: dict[str, Any] | None = None
    calculated_values: dict[str, Any] | None = None
    error: str | None = None


@router.post("/buy", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_buy_order(request: RiskManagedOrderRequest) -> OrderResponse:
    """
    Place a BUY market order with automatic stop loss.

    The stop loss is calculated as the lowest low of the last N candles
    of the specified timeframe. Position size is calculated based on
    risk_per_trade and the stop loss distance.

    Returns:
        OrderResponse with order details and calculated values.
    """
    try:
        # Prepare additional parameters
        additional_params: dict[str, Any] = {}
        if request.reduce_only is not None:
            additional_params["reduce_only"] = request.reduce_only
        if request.time_in_force is not None:
            additional_params["time_in_force"] = request.time_in_force
        if request.client_order_id is not None:
            additional_params["client_order_id"] = request.client_order_id

        # Place the risk-managed order
        result = place_risk_managed_market_order(
            side="buy",
            product_id=request.product_id,
            product_symbol=request.product_symbol,
            risk_per_trade=request.risk_per_trade,
            timeframe=request.timeframe,
            candles_count=request.candles_count,
            **additional_params,
        )

        return OrderResponse(
            success=True,
            message="BUY order placed successfully",
            market_order=result.get("market_order"),
            stop_loss_order=result.get("stop_loss_order"),
            calculated_values=result.get("calculated_values"),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to place order: {str(e)}",
        ) from e


@router.post("/sell", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_sell_order(request: RiskManagedOrderRequest) -> OrderResponse:
    """
    Place a SELL market order with automatic stop loss.

    The stop loss is calculated as the highest high of the last N candles
    of the specified timeframe. Position size is calculated based on
    risk_per_trade and the stop loss distance.

    Returns:
        OrderResponse with order details and calculated values.
    """
    try:
        # Prepare additional parameters
        additional_params: dict[str, Any] = {}
        if request.reduce_only is not None:
            additional_params["reduce_only"] = request.reduce_only
        if request.time_in_force is not None:
            additional_params["time_in_force"] = request.time_in_force
        if request.client_order_id is not None:
            additional_params["client_order_id"] = request.client_order_id

        # Place the risk-managed order
        result = place_risk_managed_market_order(
            side="sell",
            product_id=request.product_id,
            product_symbol=request.product_symbol,
            risk_per_trade=request.risk_per_trade,
            timeframe=request.timeframe,
            candles_count=request.candles_count,
            **additional_params,
        )

        return OrderResponse(
            success=True,
            message="SELL order placed successfully",
            market_order=result.get("market_order"),
            stop_loss_order=result.get("stop_loss_order"),
            calculated_values=result.get("calculated_values"),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to place order: {str(e)}",
        ) from e

