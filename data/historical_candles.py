"""
Historical candles data retrieval and processing.

This module provides functions to fetch historical OHLC candle data
from Delta Exchange and convert it to pandas DataFrames with proper
datetime processing.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Union

import pandas as pd

from config import get_client


def get_historical_candles(
    resolution: str,
    symbol: str,
    start: Union[int, str, datetime],
    end: Union[int, str, datetime],
    **filters: Any,
) -> pd.DataFrame:
    """
    Retrieve historical OHLC candles and return as a pandas DataFrame.

    The time column is automatically converted to datetime with proper timezone
    handling. The DataFrame is sorted by time in ascending order.

    Parameters
    ----------
    resolution : str
        Candle resolution (e.g., '1m', '5m', '15m', '1h', '1d').
    symbol : str
        Trading symbol (e.g., 'BTCUSD').
    start : int, str, or datetime
        Start timestamp (Unix timestamp in seconds) or datetime object.
        If datetime, will be converted to Unix timestamp.
    end : int, str, or datetime
        End timestamp (Unix timestamp in seconds) or datetime object.
        If datetime, will be converted to Unix timestamp.
    **filters : Any
        Additional filters to pass to the API request.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - time: datetime64[ns] (converted from Unix timestamp)
        - open: float
        - high: float
        - low: float
        - close: float
        - volume: float

        The DataFrame is sorted by time in ascending order.

    Raises
    ------
    ValueError
        If the API response is not successful or missing expected data.
    """
    client = get_client()

    # Convert datetime objects to Unix timestamps if needed
    if isinstance(start, datetime):
        start = int(start.timestamp())
    elif isinstance(start, str):
        try:
            start = int(start)
        except ValueError:
            # Try parsing as datetime string
            start_dt = pd.to_datetime(start)
            start = int(start_dt.timestamp())

    if isinstance(end, datetime):
        end = int(end.timestamp())
    elif isinstance(end, str):
        try:
            end = int(end)
        except ValueError:
            # Try parsing as datetime string
            end_dt = pd.to_datetime(end)
            end = int(end_dt.timestamp())

    # Call the API
    response = client.get_historical_candles(
        resolution=resolution,
        symbol=symbol,
        start=start,
        end=end,
        **filters,
    )

    # Validate response
    if not response.get("success", False):
        raise ValueError(
            f"API request failed: {response.get('message', 'Unknown error')}"
        )

    result = response.get("result", [])
    if not result:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(
            columns=["time", "open", "high", "low", "close", "volume"]
        )

    # Convert to DataFrame
    df = pd.DataFrame(result)

    # Convert time column from Unix timestamp to datetime
    if "time" in df.columns:
        # Assuming time is in seconds (Unix timestamp)
        df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
        # Convert to timezone-naive datetime (or keep UTC based on preference)
        # df["time"] = df["time"].dt.tz_localize(None)  # Uncomment to remove timezone

    # Ensure numeric columns are float
    numeric_columns = ["open", "high", "low", "close", "volume"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort by time
    df = df.sort_values("time").reset_index(drop=True)

    return df

