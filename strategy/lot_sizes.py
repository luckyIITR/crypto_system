"""
Lot size definitions for different trading products.

Lot sizes define the minimum tradeable unit for each product.
"""

from __future__ import annotations

# Lot size definitions (1 LOT = X base currency)
LOT_SIZES: dict[str, float] = {
    "BTCUSD": 0.001,  # 1 LOT = 0.001 BTC
    "ETHUSD": 0.01,   # 1 LOT = 0.01 ETH
    # Add more products as needed
    # Format: "SYMBOL": lot_size_in_base_currency
}

# Common BTC product symbols variations
BTC_SYMBOLS = ["BTCUSD", "BTC-USD", "BTC_USD", "BTCUSD-PERP"]

# Common ETH product symbols variations
ETH_SYMBOLS = ["ETHUSD", "ETH-USD", "ETH_USD", "ETHUSD-PERP"]


def get_lot_size(product_symbol: str | None = None, product_id: int | None = None) -> float:
    """
    Get the lot size for a given product.

    Parameters
    ----------
    product_symbol : str, optional
        Product symbol (e.g., 'BTCUSD', 'ETHUSD').
    product_id : int, optional
        Product ID (currently not used, but kept for future expansion).

    Returns
    -------
    float
        Lot size in base currency. Defaults to 1.0 if product not found.

    Examples
    --------
    >>> get_lot_size(product_symbol="BTCUSD")
    0.001
    >>> get_lot_size(product_symbol="ETHUSD")
    0.01
    >>> get_lot_size(product_symbol="UNKNOWN")
    1.0
    """
    if product_symbol is None:
        return 1.0  # Default lot size

    # Normalize symbol (uppercase, remove common separators)
    normalized_symbol = product_symbol.upper().replace("-", "").replace("_", "")

    # Check direct match
    if normalized_symbol in LOT_SIZES:
        return LOT_SIZES[normalized_symbol]

    # Check BTC variations
    if any(btc_symbol.replace("-", "").replace("_", "") == normalized_symbol for btc_symbol in BTC_SYMBOLS):
        return LOT_SIZES["BTCUSD"]

    # Check ETH variations
    if any(eth_symbol.replace("-", "").replace("_", "") == normalized_symbol for eth_symbol in ETH_SYMBOLS):
        return LOT_SIZES["ETHUSD"]

    # Default to 1.0 if not found
    return 1.0


def convert_to_lots(quantity: float, lot_size: float) -> int:
    """
    Convert a quantity in base currency to lots.

    Parameters
    ----------
    quantity : float
        Quantity in base currency.
    lot_size : float
        Size of one lot in base currency.

    Returns
    -------
    int
        Number of lots (rounded down).

    Examples
    --------
    >>> convert_to_lots(0.005, 0.001)  # 0.005 BTC / 0.001 = 5 lots
    5
    >>> convert_to_lots(0.05, 0.01)    # 0.05 ETH / 0.01 = 5 lots
    5
    """
    if lot_size <= 0:
        raise ValueError("Lot size must be greater than 0")
    return int(quantity / lot_size)


def convert_from_lots(lots: int, lot_size: float) -> float:
    """
    Convert lots to base currency quantity.

    Parameters
    ----------
    lots : int
        Number of lots.
    lot_size : float
        Size of one lot in base currency.

    Returns
    -------
    float
        Quantity in base currency.

    Examples
    --------
    >>> convert_from_lots(5, 0.001)  # 5 lots * 0.001 = 0.005 BTC
    0.005
    >>> convert_from_lots(5, 0.01)   # 5 lots * 0.01 = 0.05 ETH
    0.05
    """
    return lots * lot_size

