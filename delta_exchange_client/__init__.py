"""
Python client library for interacting with the Delta Exchange REST API.

The client surfaces higher-level helpers for common tasks such as retrieving
open orders and placing new orders while taking care of request signing,
headers, retries and error handling.
"""

from .client import DeltaExchangeClient

__all__ = ["DeltaExchangeClient"]

