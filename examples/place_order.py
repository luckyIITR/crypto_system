"""
Example script: place a complex order on Delta Exchange.

Usage:
    # ensure .env sits at repo root with DELTA_API_KEY/DELTA_API_SECRET
    python examples/place_order.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv

from delta_exchange_client import DeltaExchangeClient


def main() -> None:
    load_dotenv(ROOT_DIR / ".env")

    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    if not api_key or not api_secret:
        raise SystemExit(
            "Set DELTA_API_KEY and DELTA_API_SECRET environment variables first."
        )

    client = DeltaExchangeClient(api_key=api_key, api_secret=api_secret)

    order_params = {
        "product_id": 27,
        "product_symbol": "BTCUSD",
        "limit_price": "101100",
        "size": 1,
        "side": "buy",
        "order_type": "limit_order"
    }

    response = client.place_order(**order_params)
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - demo script
        print(f"Order placement failed: {exc}", file=sys.stderr)
        sys.exit(1)

