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
- `get_order_history(...)`
- `change_order_leverage(product_id, leverage=...)`
- `get_order_leverage(product_id)`
- `get_historical_candles(...)`
- `get_sparklines(...)`
- `get_positions(...)` / `get_margined_positions(...)`
- `set_position_auto_topup(...)` / `change_position_margin(...)`
- `close_all_positions(...)`

See `docs/orders.md`, `docs/positions.md`, `docs/trade_history.md`, and `docs/history.md` for detailed endpoint walkthroughs and payload examples.

## API Server

The project includes a FastAPI server for placing risk-managed orders via REST API.

### Start the API Server

```bash
python run_api.py
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Interactive Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Full API Documentation**: See `docs/api.md`

### Quick API Example

```bash
# Place a BUY order
curl -X POST "http://localhost:8000/api/v1/orders/buy" \
  -H "Content-Type: application/json" \
  -d '{
    "product_symbol": "BTCUSD",
    "risk_per_trade": 100.0
  }'
```

For complete API documentation, see `docs/api.md`.

