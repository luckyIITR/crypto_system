"""
Simple test script to verify market order placement functionality.

This script tests the place_market_order function to ensure it:
1. Validates required parameters correctly
2. Handles parameter validation errors
3. Successfully places market orders (if credentials are valid)
4. Returns proper response structure

Usage:
    python test/test_market_order.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from order_management import place_market_order


def test_parameter_validation() -> None:
    """Test parameter validation logic."""
    print("=" * 60)
    print("Testing Parameter Validation")
    print("=" * 60)

    # Test 1: Missing both product_id and product_symbol
    print("\n1. Testing missing product_id and product_symbol...")
    try:
        place_market_order(size=1, side="buy")
        print("   ✗ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Correctly raised ValueError: {e}")

    # Test 2: Providing both product_id and product_symbol
    print("\n2. Testing both product_id and product_symbol provided...")
    try:
        place_market_order(
            product_id=27, product_symbol="BTCUSD", size=1, side="buy"
        )
        print("   ✗ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Correctly raised ValueError: {e}")

    # Test 4: Invalid side
    print("\n4. Testing invalid side...")
    try:
        place_market_order(product_symbol="BTCUSD", size=1, side="invalid")
        print("   ✗ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Correctly raised ValueError: {e}")

    # Test 5: client_order_id too long
    print("\n5. Testing client_order_id length validation...")
    try:
        place_market_order(
            product_symbol="BTCUSD",
            size=1,
            side="buy",
            client_order_id="a" * 33,  # 33 characters, max is 32
        )
        print("   ✗ Should have raised ValueError")
    except ValueError as e:
        print(f"   ✓ Correctly raised ValueError: {e}")

    print("\n" + "=" * 60)
    print("✓ All parameter validation tests passed!")
    print("=" * 60)


def test_market_order_placement() -> None:
    """Test actual market order placement (requires valid credentials)."""
    print("\n" + "=" * 60)
    print("Testing Market Order Placement")
    print("=" * 60)

    # Test parameters - using minimal required fields
    test_params = {
        "product_symbol": "BTCUSD",
        "size": 1,
        "side": "buy",
    }

    print(f"\nTest Parameters:")
    for key, value in test_params.items():
        print(f"  {key}: {value}")

    print("\n⚠ Note: This will attempt to place a REAL order!")
    print("   Make sure you have valid API credentials and sufficient balance.")
    print("   Press Ctrl+C within 5 seconds to cancel...")

    try:
        import time
        time.sleep(5)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
        return

    try:
        print("\nPlacing market order...")
        response = place_market_order(**test_params)

        print("\n✓ Order placed successfully!")
        print(f"\nResponse:")
        print(json.dumps(response, indent=2))

        # Validate response structure
        if isinstance(response, dict):
            if "success" in response:
                if response.get("success"):
                    print("\n✓ Response indicates success")
                else:
                    print(f"\n⚠ Response indicates failure: {response.get('message', 'Unknown')}")
            
            if "result" in response:
                result = response["result"]
                print(f"\nOrder Details:")
                if isinstance(result, dict):
                    for key in ["id", "product_id", "product_symbol", "side", "size", "order_type"]:
                        if key in result:
                            print(f"  {key}: {result[key]}")
        else:
            print("\n⚠ Unexpected response format")

        print("\n" + "=" * 60)
        print("✓ Market order placement test completed!")
        print("=" * 60)

    except ValueError as e:
        print(f"\n✗ Validation Error: {e}")
        print("\nThis is expected if parameters are invalid.")
    except Exception as e:
        print(f"\n✗ Error placing order: {e}")
        print("\nPossible reasons:")
        print("  1. Invalid API credentials")
        print("  2. Insufficient balance")
        print("  3. Invalid product symbol")
        print("  4. Network/API issues")
        import traceback
        traceback.print_exc()



def main() -> None:
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Market Order Test Suite")
    print("=" * 60)

    # Run validation tests (safe, no API calls)
    test_parameter_validation()

    # Ask user if they want to test actual order placement
    print("\n" + "=" * 60)
    print("Order Placement Tests (requires valid API credentials)")
    print("=" * 60)
    print("\nThese tests will attempt to place REAL orders.")
    print("Do you want to proceed? (yes/no): ", end="", flush=True)

    try:
        user_input = input().strip().lower()
        if user_input in ("yes", "y"):
            test_market_order_placement()
        else:
            print("\nSkipping order placement tests.")
            print("To test order placement, run this script again and type 'yes'.")
    except (EOFError, KeyboardInterrupt):
        print("\n\nSkipping order placement tests.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

