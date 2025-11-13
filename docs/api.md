# Crypto Trading System API Documentation

## Overview

The Crypto Trading System API provides endpoints for placing risk-managed market orders with automatic stop loss calculation. The API uses FastAPI and provides automatic interactive documentation.

**Base URL**: `http://localhost:8000`

**API Version**: `v1`

## Quick Start

### Start the Server

```bash
python run_api.py
```

Or using uvicorn directly:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Health Check

Check if the API is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy"
}
```

**Example**:
```bash
curl http://localhost:8000/health
```

---

### Root Endpoint

Get API information.

**Endpoint**: `GET /`

**Response**:
```json
{
  "message": "Crypto Trading System API"
}
```

---

## Order Management

### Place BUY Order

Place a BUY market order with automatic stop loss calculation.

**Endpoint**: `POST /api/v1/orders/buy`

**Description**: 
- Places a market BUY order
- Calculates stop loss as the **lowest low** of the last N candles
- Calculates position size based on risk per trade and stop loss distance
- Automatically places a stop loss order

**Request Body**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `product_id` | integer | No* | - | Product ID (only one of product_id or product_symbol required) |
| `product_symbol` | string | No* | - | Product symbol (e.g., "BTCUSD") (only one of product_id or product_symbol required) |
| `risk_per_trade` | float | Yes | - | Risk amount per trade (in base currency). Must be > 0 |
| `timeframe` | string | No | "5m" | Candle timeframe (e.g., "5m", "15m", "1h") |
| `candles_count` | integer | No | 5 | Number of candles to analyze (1-100) |
| `reduce_only` | string | No | - | If set, will only close positions |
| `time_in_force` | string | No | - | Order type: "GTC" or "IOC" |
| `client_order_id` | string | No | - | Custom order ID (max 32 characters) |

\* Either `product_id` or `product_symbol` must be provided, but not both.

**Request Example**:
```json
{
  "product_symbol": "BTCUSD",
  "risk_per_trade": 100.0,
  "timeframe": "5m",
  "candles_count": 5
}
```

**Response** (201 Created):

```json
{
  "success": true,
  "message": "BUY order placed successfully",
  "market_order": {
    "success": true,
    "result": {
      "id": 12345678,
      "product_id": 27,
      "product_symbol": "BTCUSD",
      "side": "buy",
      "size": 10,
      "order_type": "market_order",
      "state": "filled",
      ...
    }
  },
  "stop_loss_order": {
    "success": true,
    "result": {
      "id": 12345679,
      "order_type": "stop_order",
      "stop_price": "50000.00",
      ...
    }
  },
  "calculated_values": {
    "current_price": 51000.00,
    "stop_loss_price": 50000.00,
    "sl_points": 1000.00,
    "risk_per_trade": 100.0,
    "position_size": 10,
    "timeframe": "5m",
    "candles_count": 5,
    "side": "buy"
  },
  "error": null
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/orders/buy" \
  -H "Content-Type: application/json" \
  -d '{
    "product_symbol": "BTCUSD",
    "risk_per_trade": 100.0,
    "timeframe": "5m",
    "candles_count": 5
  }'
```

**Python Example**:
```python
import requests

url = "http://localhost:8000/api/v1/orders/buy"
payload = {
    "product_symbol": "BTCUSD",
    "risk_per_trade": 100.0,
    "timeframe": "5m",
    "candles_count": 5
}

response = requests.post(url, json=payload)
print(response.json())
```

**Error Responses**:

- **400 Bad Request**: Invalid parameters
```json
{
  "detail": "Either product_id or product_symbol must be provided."
}
```

- **500 Internal Server Error**: Order placement failed
```json
{
  "detail": "Failed to place order: Insufficient balance"
}
```

---

### Place SELL Order

Place a SELL market order with automatic stop loss calculation.

**Endpoint**: `POST /api/v1/orders/sell`

**Description**: 
- Places a market SELL order
- Calculates stop loss as the **highest high** of the last N candles
- Calculates position size based on risk per trade and stop loss distance
- Automatically places a stop loss order

**Request Body**: Same as BUY order endpoint

**Request Example**:
```json
{
  "product_symbol": "BTCUSD",
  "risk_per_trade": 100.0,
  "timeframe": "5m",
  "candles_count": 5,
  "reduce_only": "true"
}
```

**Response** (201 Created): Same structure as BUY order response

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/orders/sell" \
  -H "Content-Type: application/json" \
  -d '{
    "product_symbol": "BTCUSD",
    "risk_per_trade": 100.0,
    "timeframe": "5m",
    "candles_count": 5
  }'
```

---

## How It Works

### Stop Loss Calculation

The API automatically calculates stop loss levels based on recent candle data:

1. **For BUY orders**: 
   - Stop Loss = Lowest low of last N candles
   - Protects against downward price movement

2. **For SELL orders**:
   - Stop Loss = Highest high of last N candles
   - Protects against upward price movement

### Position Sizing

Position size is calculated using the formula:

```
SL Points = |Current Market Price - Stop Loss Price|
Position Size = Risk Per Trade / SL Points
```

The position size is rounded down to the nearest integer (as required by the exchange).

### Example Calculation

**BUY Order Example**:
- Current Price: $51,000
- Last 5 candles lows: [50,500, 50,600, 50,400, 50,550, 50,300]
- Stop Loss Price: $50,300 (lowest low)
- SL Points: |51,000 - 50,300| = $700
- Risk Per Trade: $100
- Position Size: 100 / 700 = 0.142 → **0** (rounded down)

**Note**: If calculated position size is 0, the API will return an error.

---

## Request/Response Models

### RiskManagedOrderRequest

```json
{
  "product_id": 27,                    // Optional: integer
  "product_symbol": "BTCUSD",           // Optional: string
  "risk_per_trade": 100.0,             // Required: float > 0
  "timeframe": "5m",                   // Optional: string (default: "5m")
  "candles_count": 5,                  // Optional: integer 1-100 (default: 5)
  "reduce_only": "true",               // Optional: string
  "time_in_force": "IOC",              // Optional: string ("GTC" or "IOC")
  "client_order_id": "my_order_123"    // Optional: string (max 32 chars)
}
```

### OrderResponse

```json
{
  "success": true,                      // boolean
  "message": "BUY order placed successfully",  // string
  "market_order": { ... },             // object: Market order details
  "stop_loss_order": { ... },         // object: Stop loss order details
  "calculated_values": {               // object: Calculated values
    "current_price": 51000.00,
    "stop_loss_price": 50000.00,
    "sl_points": 1000.00,
    "risk_per_trade": 100.0,
    "position_size": 10,
    "timeframe": "5m",
    "candles_count": 5,
    "side": "buy"
  },
  "error": null                        // string | null
}
```

---

## Error Handling

The API uses standard HTTP status codes:

- **200 OK**: Successful request
- **201 Created**: Order successfully placed
- **400 Bad Request**: Invalid request parameters
- **500 Internal Server Error**: Server error or order placement failure

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Configuration

### Environment Variables

The API requires the following environment variables (set in `.env` file):

```
DELTA_API_KEY=your_api_key_here
DELTA_API_SECRET=your_api_secret_here
```

### API Configuration

Default server configuration:
- **Host**: `0.0.0.0` (all interfaces)
- **Port**: `8000`
- **Reload**: Enabled (auto-reload on code changes)

To change the port, modify `run_api.py`:

```python
uvicorn.run(
    "api.main:app",
    host="0.0.0.0",
    port=8080,  # Change port here
    reload=True,
)
```

---

## Best Practices

1. **Always check the response**: Verify `success: true` before assuming the order was placed
2. **Handle errors gracefully**: Check for `error` field in response
3. **Use appropriate risk_per_trade**: Ensure it's sufficient to calculate a valid position size
4. **Monitor stop_loss_order**: Verify that the stop loss order was placed successfully
5. **Use client_order_id**: For tracking orders in your system
6. **Test with small amounts**: Always test with small risk_per_trade values first

---

## Rate Limiting

Currently, there are no rate limits implemented. However, be mindful of:
- Exchange API rate limits
- Network latency
- Order processing time

---

## Support

For issues or questions:
1. Check the interactive documentation at `/docs`
2. Review error messages in the response
3. Verify API credentials are correct
4. Ensure sufficient balance for orders

---

## Changelog

### Version 1.0.0
- Initial release
- BUY and SELL order endpoints
- Automatic stop loss calculation
- Risk-based position sizing

