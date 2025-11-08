# Delta Exchange Client

Thin Python client for the Delta Exchange REST API that handles request signing and common order endpoints.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root containing:

```
DELTA_API_KEY=your_api_key
DELTA_API_SECRET=your_api_secret
```

## Usage

```python
from delta_exchange_client import DeltaExchangeClient

client = DeltaExchangeClient(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
)

open_orders = client.get_active_orders(product_id=1, state="open")
created_order = client.place_order(
    order_type="limit_order",
    size=3,
    side="buy",
    limit_price="0.0005",
    product_id=16,
)

client.edit_order(order_id=created_order["result"]["id"], size=5)
client.cancel_order(order_id=created_order["result"]["id"])
```

For a runnable example see `examples/place_order.py`.

### Additional helpers

- `place_bracket_order(...)` / `edit_bracket_order(...)`
- `cancel_all_orders(...)`
- `get_order(order_id)`
- `change_order_leverage(product_id, leverage=...)`
- `get_order_leverage(product_id)`

See `docs/orders.md` for detailed endpoint walkthroughs and payload examples.

