"""
Centralized Delta Exchange client instance.

This module provides a singleton client instance that can be reused
across different parts of the algorithm to avoid multiple initializations
and ensure consistent configuration.

Usage:
    from config import get_client
    
    client = get_client()
    orders = client.get_active_orders()
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from delta_exchange_client import DeltaExchangeClient

# Load environment variables from .env file at project root
ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

# Global client instance (singleton pattern)
_client: Optional[DeltaExchangeClient] = None


def get_client() -> DeltaExchangeClient:
    """
    Get or create the centralized Delta Exchange client instance.

    This function implements a singleton pattern to ensure only one client
    instance exists throughout the application lifecycle. The client is
    lazily initialized on first access.

    The client is initialized using environment variables:
    - DELTA_API_KEY: API key for Delta Exchange
    - DELTA_API_SECRET: API secret for Delta Exchange

    Returns
    -------
    DeltaExchangeClient
        The initialized client instance. Subsequent calls return the same
        instance.

    Raises
    ------
    ValueError
        If DELTA_API_KEY or DELTA_API_SECRET are not set in environment
        variables or .env file.

    Examples
    --------
    >>> from config import get_client
    >>> client = get_client()
    >>> orders = client.get_active_orders()
    """
    global _client

    if _client is None:
        api_key = os.getenv("DELTA_API_KEY")
        api_secret = os.getenv("DELTA_API_SECRET")

        if not api_key or not api_secret:
            raise ValueError(
                "DELTA_API_KEY and DELTA_API_SECRET must be set in environment "
                "variables or .env file. Please ensure your .env file exists "
                "at the project root with these variables defined."
            )

        _client = DeltaExchangeClient(api_key=api_key, api_secret=api_secret)

    return _client


def reset_client() -> None:
    """
    Reset the global client instance.

    This function clears the cached client instance, forcing a new
    initialization on the next call to get_client(). Useful for:
    - Testing scenarios where you need fresh instances
    - Refreshing credentials without restarting the application
    - Handling credential rotation

    Examples
    --------
    >>> from config import reset_client, get_client
    >>> reset_client()  # Clear existing instance
    >>> client = get_client()  # Creates new instance with updated credentials
    """
    global _client
    _client = None


def is_initialized() -> bool:
    """
    Check if the client has been initialized.

    Returns
    -------
    bool
        True if the client has been initialized, False otherwise.
    """
    return _client is not None

