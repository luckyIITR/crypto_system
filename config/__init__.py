"""
Configuration module for the crypto trading system.

This module provides centralized configuration and client initialization.
"""

from .client import get_client, is_initialized, reset_client

__all__ = ["get_client", "reset_client", "is_initialized"]

