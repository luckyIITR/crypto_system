# Historical Market Data Guide

Fetch OHLC candles and sparklines using `DeltaExchangeClient`.

```python
from delta_exchange_client import DeltaExchangeClient

client = DeltaExchangeClient(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
)
```

## Historical OHLC Candles (`GET /v2/history/candles`)

```python
response = client.get_historical_candles(
    resolution="5m",
    symbol="BTCUSD",
    start=1685618835,
    end=1722511635,
)
```

- `resolution` supports values like `1m`, `5m`, `1h`, `1d`, etc.
- `start` and `end` accept UNIX timestamps (ints or strings).
- Up to 2,000 candles are returned per request. Paginate by adjusting the range.
- Additional query fields can be supplied via keyword arguments.

## Sparklines (`GET /v2/history/sparklines`)

```python
response = client.get_sparklines(symbols=["ETHUSD", "MARK:BTCUSD"])
```

Alternatively, pass a comma-separated string:

```python
response = client.get_sparklines(symbols="ETHUSD,MARK:BTCUSD")
```

Use extra keyword arguments to pass through optional query parameters supported by the API (e.g. time ranges or product type filters).

