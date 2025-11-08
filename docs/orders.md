# Orders API Guide

This guide walks through the order-management helpers exposed by `delta_exchange_client.DeltaExchangeClient`. Each method wraps a corresponding Delta Exchange REST endpoint and takes care of HMAC signing, headers, and request retries.

- All methods require that you instantiate `DeltaExchangeClient` with valid API credentials.
- Boolean arguments should be passed as Python `True` / `False`; the client converts them to the string values expected by the API.
- Numerical arguments may be passed as either `int`, `float`, or strings; the API ultimately receives their string representation.

```python
from delta_exchange_client import DeltaExchangeClient

client = DeltaExchangeClient(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
)
```

## Place Order (`POST /v2/orders`)

```python
response = client.place_order(
    product_id=27,
    product_symbol="BTCUSD",
    limit_price="59000",
    size=10,
    side="buy",
    order_type="limit_order",
    stop_order_type="stop_loss_order",
    stop_price="56000",
    trail_amount="50",
    stop_trigger_method="last_traded_price",
    bracket_stop_trigger_method="last_traded_price",
    bracket_stop_loss_limit_price="57000",
    bracket_stop_loss_price="56000",
    bracket_trail_amount="50",
    bracket_take_profit_limit_price="62000",
    bracket_take_profit_price="61000",
    time_in_force="gtc",
    mmp="disabled",
    post_only=False,
    reduce_only=False,
    client_order_id="my_signal_345212",
    cancel_orders_accepted=False,
)
```

Returns the raw JSON payload from Delta Exchange that includes the created order.

## Cancel Order (`DELETE /v2/orders`)

```python
response = client.cancel_order(
    order_id=13452112,
    client_order_id="my_signal_34521712",
    product_id=27,
)
```

Provide at least one identifier (`order_id` or `client_order_id`). `product_id` can be supplied to scope the cancel request.

## Edit Order (`PUT /v2/orders`)

```python
response = client.edit_order(
    order_id=34521712,
    product_id=27,
    product_symbol="BTCUSD",
    limit_price="59000",
    size=15,
    mmp="disabled",
    post_only=False,
    cancel_orders_accepted=False,
    stop_price="56000",
    trail_amount="50",
)
```

Supply the order identifier plus the fields you would like to update. The client passes them through unchanged.

## Get Active Orders (`GET /v2/orders`)

```python
response = client.get_active_orders(product_id=27, state="open")
```

If no filters are supplied, all active orders for the account are returned.

## Place Bracket Order (`POST /v2/orders/bracket`)

```python
response = client.place_bracket_order(
    product_id=27,
    product_symbol="BTCUSD",
    stop_loss_order={
        "order_type": "limit_order",
        "stop_price": "56000",
        "trail_amount": "50",
        "limit_price": "55000",
    },
    take_profit_order={
        "order_type": "limit_order",
        "stop_price": "65000",
        "limit_price": "64000",
    },
    bracket_stop_trigger_method="last_traded_price",
)
```

Nested dictionaries are serialized automatically and included in the signed payload.

## Edit Bracket Order (`PUT /v2/orders/bracket`)

```python
response = client.edit_bracket_order(
    id=34521712,
    product_id=27,
    product_symbol="BTCUSD",
    bracket_stop_loss_limit_price="55000",
    bracket_stop_loss_price="56000",
    bracket_take_profit_limit_price="65000",
    bracket_take_profit_price="64000",
    bracket_trail_amount="50",
    bracket_stop_trigger_method="last_traded_price",
)
```

Any provided fields are merged into the existing bracket order.

## Cancel All Orders (`DELETE /v2/orders/all`)

```python
response = client.cancel_all_orders(
    product_id=27,
    contract_types="perpetual_futures,put_options,call_options",
    cancel_limit_orders=False,
    cancel_stop_orders=False,
    cancel_reduce_only_orders=False,
)
```

Use filters to control which open orders are cancelled.

## Get Order by ID (`GET /v2/orders/{order_id}`)

```python
response = client.get_order(order_id=34521712)
```

Returns a single order resource.

## Change Order Leverage (`POST /v2/products/{product_id}/orders/leverage`)

```python
response = client.change_order_leverage(product_id=27, leverage=10)
```

Sets the leverage that will be applied to subsequent orders for the product.

## Get Order Leverage (`GET /v2/products/{product_id}/orders/leverage`)

```python
response = client.get_order_leverage(product_id=27)
```

Retrieves the leverage configuration currently in effect for the given product.

