"""
Delta Exchange REST API client.

The official API documentation:
https://docs.delta.exchange/#get-open-orders
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import time
from typing import Any, Dict, Mapping, Optional, Union

import requests
from requests import Response, Session
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import urlencode

DEFAULT_TIMEOUT = (3.0, 30.0)


class DeltaExchangeClientError(Exception):
    """Base error for all client related failures."""


class DeltaExchangeRequestError(DeltaExchangeClientError):
    """Raised when the API returns an HTTP error response."""

    def __init__(self, response: Response):
        super().__init__(
            f"Delta Exchange API returned {response.status_code}: {response.text}"
        )
        self.response = response


class DeltaExchangeClient:
    """
    Thin HTTP client that authenticates and signs requests for the Delta Exchange API.

    Parameters
    ----------
    api_key:
        API key issued by Delta Exchange.
    api_secret:
        API secret used when signing requests.
    base_url:
        Base REST API URL. Defaults to the production endpoint.
    session:
        Optional preconfigured `requests.Session` instance.
    timeout:
        Optional timeout tuple `(connect_timeout, read_timeout)`.
    user_agent:
        Overrides the default user-agent header.
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        *,
        base_url: str = "https://api.india.delta.exchange",
        session: Optional[Session] = None,
        timeout: Union[float, tuple[float, float]] = DEFAULT_TIMEOUT,
        user_agent: str = "delta-exchange-python-client/0.1.0",
        enable_retries: bool = True,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.timeout = (
            float(timeout)
            if isinstance(timeout, (int, float))
            else (float(timeout[0]), float(timeout[1]))
        )
        self.user_agent = user_agent
        self.session = session or self._build_default_session(enable_retries)

    def _build_default_session(self, enable_retries: bool) -> Session:
        session = requests.Session()
        if enable_retries:
            retry = Retry(
                total=3,
                backoff_factor=0.3,
                status_forcelist=(429, 500, 502, 503, 504),
                allowed_methods=["GET", "POST", "DELETE", "PUT"],
                raise_on_status=False,
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("https://", adapter)
            session.mount("http://", adapter)
        return session

    def _generate_signature(self, message: str) -> str:
        message_bytes = message.encode()
        secret_bytes = self.api_secret.encode()
        return hmac.new(secret_bytes, message_bytes, hashlib.sha256).hexdigest()

    def _build_headers(self, timestamp: str, signature: str) -> Dict[str, str]:
        return {
            "api-key": self.api_key,
            "timestamp": timestamp,
            "signature": signature,
            "User-Agent": self.user_agent,
            "Content-Type": "application/json",
        }

    def _stringify_param_value(self, value: Any) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            return value
        return json.dumps(value, separators=(",", ":"), sort_keys=True)

    def _normalize_params(
        self, params: Optional[Mapping[str, Any]]
    ) -> tuple[Optional[list[tuple[str, str]]], str]:
        if not params:
            return None, ""

        normalized: list[tuple[str, str]] = []
        for key in sorted(params):
            value = params[key]
            if value is None:
                continue
            if isinstance(value, (list, tuple, set)):
                for element in value:
                    normalized.append((key, self._stringify_param_value(element)))
            else:
                normalized.append((key, self._stringify_param_value(value)))

        if not normalized:
            return None, ""

        query_string = "?" + urlencode(normalized, doseq=True)
        return normalized, query_string

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        data: Optional[Union[str, Mapping[str, Any]]] = None,
        require_auth: bool = True,
    ) -> Response:
        method_upper = method.upper()
        timestamp = str(int(time.time()))
        normalized_params, query_string = self._normalize_params(params)

        json_payload = ""
        data_payload: Optional[str]

        if data is None:
            data_payload = None
        elif isinstance(data, (dict, list)):
            json_payload = json.dumps(data, separators=(",", ":"), sort_keys=True)
            data_payload = json_payload
        else:
            json_payload = str(data)
            data_payload = json_payload

        signature_payload = (
            method_upper + timestamp + path + query_string + json_payload
            if require_auth
            else ""
        )
        signature = (
            self._generate_signature(signature_payload) if require_auth else ""
        )
        headers = (
            self._build_headers(timestamp, signature) if require_auth else {}
        )

        url = f"{self.base_url}{path}"
        logging.debug(
            "Sending request %s %s params=%s payload=%s",
            method_upper,
            url,
            params,
            json_payload if json_payload else None,
        )

        response = self.session.request(
            method_upper,
            url,
            params=normalized_params,
            data=data_payload,
            timeout=self.timeout,
            headers=headers,
        )
        if not response.ok:
            logging.error(
                "Delta Exchange API error %s: %s", response.status_code, response.text
            )
            raise DeltaExchangeRequestError(response)
        return response

    def _extract_json(self, response: Response) -> Any:
        try:
            return response.json()
        except ValueError as exc:
            raise DeltaExchangeClientError(
                "Failed to parse JSON response from Delta Exchange API"
            ) from exc

    def place_order(self, **order_params: Any) -> Any:
        """
        Place a new order.

        The parameters map directly to the Delta Exchange REST API payload.
        """
        if not order_params:
            raise ValueError("order_params must include at least one field")

        response = self._request("POST", "/v2/orders", data=order_params)
        return self._extract_json(response)

    def cancel_order(
        self,
        *,
        order_id: Optional[Union[int, str]] = None,
        client_order_id: Optional[str] = None,
        product_id: Optional[Union[int, str]] = None,
    ) -> Any:
        """
        Cancel an order using its id or client order identifier.
        """
        params: Dict[str, Any] = {}
        if order_id is not None:
            params["id"] = order_id
        if client_order_id is not None:
            params["client_order_id"] = client_order_id
        if product_id is not None:
            params["product_id"] = product_id

        if not params:
            raise ValueError("Provide at least one identifier to cancel the order.")

        response = self._request("DELETE", "/v2/orders", params=params)
        return self._extract_json(response)

    def edit_order(
        self,
        *,
        order_id: Optional[Union[int, str]] = None,
        client_order_id: Optional[str] = None,
        **updates: Any,
    ) -> Any:
        """
        Edit an existing order.
        """
        payload: Dict[str, Any] = dict(updates)
        if order_id is not None:
            payload["id"] = order_id
        if client_order_id is not None:
            payload["client_order_id"] = client_order_id

        if not payload:
            raise ValueError("Provide at least one field to update the order.")

        response = self._request("PUT", "/v2/orders", data=payload)
        return self._extract_json(response)

    def get_active_orders(self, **filters: Any) -> Any:
        """
        Retrieve active orders optionally filtered by product, state, etc.
        """
        response = self._request("GET", "/v2/orders", params=filters or None)
        return self._extract_json(response)

    def place_bracket_order(self, **order_params: Any) -> Any:
        """
        Place a bracket order.
        """
        if not order_params:
            raise ValueError("order_params must include at least one field")

        response = self._request("POST", "/v2/orders/bracket", data=order_params)
        return self._extract_json(response)

    def edit_bracket_order(self, **updates: Any) -> Any:
        """
        Edit an existing bracket order.
        """
        if not updates:
            raise ValueError("Provide at least one field to update the bracket order.")

        response = self._request("PUT", "/v2/orders/bracket", data=updates)
        return self._extract_json(response)

    def cancel_all_orders(self, **filters: Any) -> Any:
        """
        Cancel all open orders, optionally filtered by product or order type.
        """
        response = self._request("DELETE", "/v2/orders/all", params=filters or None)
        return self._extract_json(response)

    def get_order(self, order_id: Union[int, str]) -> Any:
        """
        Retrieve an order by its id.
        """
        response = self._request("GET", f"/v2/orders/{order_id}")
        return self._extract_json(response)

    def change_order_leverage(
        self, product_id: Union[int, str], *, leverage: Union[int, float]
    ) -> Any:
        """
        Update the leverage used for orders on a product.
        """
        payload = {"leverage": leverage}
        response = self._request(
            "POST", f"/v2/products/{product_id}/orders/leverage", data=payload
        )
        return self._extract_json(response)

    def get_order_leverage(self, product_id: Union[int, str]) -> Any:
        """
        Fetch the leverage used for orders on a product.
        """
        response = self._request(
            "GET", f"/v2/products/{product_id}/orders/leverage"
        )
        return self._extract_json(response)
