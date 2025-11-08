# Trade History API Guide

Methods for accessing historical order data via `DeltaExchangeClient`.

```python
from delta_exchange_client import DeltaExchangeClient

client = DeltaExchangeClient(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
)
```

## Get Order History (`GET /v2/orders/history`)

```python
response = client.get_order_history()
```

By default all historical orders are returned. Pass keyword arguments to apply filters supported by the API, for example:

```python
response = client.get_order_history(
    product_id=27,
    state="cancelled",
    start_time=1690848000,
    end_time=1691452800,
)
```

Results include both cancelled and closed orders as documented by Delta Exchange.

