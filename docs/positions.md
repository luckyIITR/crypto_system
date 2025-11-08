# Positions API Guide

Helper methods under `DeltaExchangeClient` for interacting with the positions endpoints.

Instantiate the client with your credentials:

```python
from delta_exchange_client import DeltaExchangeClient

client = DeltaExchangeClient(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
)
```

## Get Margined Positions (`GET /v2/positions/margined`)

```python
response = client.get_margined_positions()
```

Optional query parameters can be supplied as keyword arguments if you want to filter the result set.

## Get Positions (`GET /v2/positions`)

```python
response = client.get_positions(product_id=0)
```

Returns positions for the account, filtered by any provided parameters.

### Get a single position

```python
response = client.get_position(product_id=0)
```

Convenience wrapper that requests a position for the specified product.

## Toggle Auto Top-up (`PUT /v2/positions/auto_topup`)

```python
response = client.set_position_auto_topup(
    product_id=0,
    auto_topup=False,
)
```

Use `True` to enable or `False` to disable; string values (e.g. `"false"`) are also accepted.

## Change Position Margin (`POST /v2/positions/change_margin`)

```python
response = client.change_position_margin(
    product_id=0,
    delta_margin="25.0",
)
```

Increase or decrease margin by specifying `delta_margin`. Positive values add margin, negative values remove it.

## Close All Positions (`POST /v2/positions/close_all`)

```python
response = client.close_all_positions(
    close_all_portfolio=True,
    close_all_isolated=True,
    user_id=0,
)
```

Arguments are optional—omit them to rely on the API defaults. The client automatically serializes booleans to the string values the API expects and signs the request.

