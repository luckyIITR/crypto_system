"""
Simple test script to verify historical candles data retrieval.

This script tests the get_historical_candles function to ensure it:
1. Successfully retrieves data from the API
2. Returns a pandas DataFrame
3. Properly processes datetime columns
4. Contains expected columns (time, open, high, low, close, volume)

Usage:
    python test/test_historical_data.py
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from data import get_historical_candles


def test_historical_candles() -> None:
    """Test historical candles data retrieval."""
    print("=" * 60)
    print("Testing Historical Candles Data Retrieval")
    print("=" * 60)

    # Test parameters
    symbol = "BTCUSD"
    resolution = "1h"
    
    # Get data for the last 24 hours
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)

    print(f"\nTest Parameters:")
    print(f"  Symbol: {symbol}")
    print(f"  Resolution: {resolution}")
    print(f"  Start: {start_time}")
    print(f"  End: {end_time}")

    try:
        # Fetch historical data
        print("\nFetching historical candles...")
        df = get_historical_candles(
            resolution=resolution,
            symbol=symbol,
            start=start_time,
            end=end_time,
        )

        # Verify DataFrame structure
        print("\n✓ Data retrieved successfully!")
        print(f"\nDataFrame Info:")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Data types:\n{df.dtypes}")

        # Check expected columns
        expected_columns = ["time", "open", "high", "low", "close", "volume"]
        missing_columns = [col for col in expected_columns if col not in df.columns]
        
        if missing_columns:
            print(f"\n⚠ Warning: Missing columns: {missing_columns}")
        else:
            print("\n✓ All expected columns present")

        # Check datetime processing
        if "time" in df.columns:
            print(f"\n✓ Time column type: {df['time'].dtype}")
            print(f"  First timestamp: {df['time'].iloc[0] if len(df) > 0 else 'N/A'}")
            print(f"  Last timestamp: {df['time'].iloc[-1] if len(df) > 0 else 'N/A'}")

        # Display sample data
        if len(df) > 0:
            print(f"\nSample Data (first 5 rows):")
            print(df.head().to_string())
            
            print(f"\nSample Data (last 5 rows):")
            print(df.tail().to_string())
            
            # Basic statistics
            print(f"\nBasic Statistics:")
            print(df[["open", "high", "low", "close", "volume"]].describe())
        else:
            print("\n⚠ Warning: DataFrame is empty - no data returned")

        print("\n" + "=" * 60)
        print("✓ Test completed successfully!")
        print("=" * 60)

    except ValueError as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. DELTA_API_KEY and DELTA_API_SECRET are set in .env file")
        print("  2. The symbol and resolution are valid")
        print("  3. The date range is valid")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    test_historical_candles()

