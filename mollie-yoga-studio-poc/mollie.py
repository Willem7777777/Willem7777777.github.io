"""A very small Mollie API client (test mode only), built on `requests`."""
from __future__ import annotations

import os

import requests

DEFAULT_BASE_URL = os.environ.get("MOLLIE_BASE_URL", "https://api.mollie.com")


class MollieError(Exception):
    """Mollie answered with an error. `status` is the HTTP status, `detail` Mollie's explanation."""

    def __init__(self, status: int, detail: str, field: str | None = None):
        super().__init__(f"Mollie API error {status}: {detail}" + (f" (field: {field})" if field else ""))
        self.status = status
        self.detail = detail
        self.field = field


class MollieClient:
    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL, timeout: float = 10):
        if not api_key or not api_key.startswith("test_"):
            raise ValueError("MOLLIE_API_KEY must be set and start with test_ (test mode only).")
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self._base_url = base_url
        self._timeout = timeout

    def _request(self, method: str, path: str, json: dict | None = None, idempotency_key: str | None = None):
        headers = dict(self._headers)
        if idempotency_key:
            # A repeated POST with the same key within an hour returns the first answer instead of acting twice.
            headers["Idempotency-Key"] = idempotency_key
        response = requests.request(method, f"{self._base_url}{path}", json=json, headers=headers, timeout=self._timeout)
        if response.status_code >= 400:
            body = response.json() if response.content else {}
            raise MollieError(response.status_code, body.get("detail", response.reason), body.get("field"))
        return response.json() if response.content else {}

    def create_customer(self, name: str, email: str) -> dict:
        return self._request("POST", "/v2/customers", {"name": name, "email": email})

    def create_payment(self, payload: dict, idempotency_key: str | None = None) -> dict:
        return self._request("POST", "/v2/payments", payload, idempotency_key)

    def get_payment(self, payment_id: str) -> dict:
        return self._request("GET", f"/v2/payments/{payment_id}")

    def list_mandates(self, customer_id: str) -> list[dict]:
        return self._request("GET", f"/v2/customers/{customer_id}/mandates")["_embedded"]["mandates"]

    def create_subscription(self, customer_id: str, payload: dict, idempotency_key: str | None = None) -> dict:
        return self._request("POST", f"/v2/customers/{customer_id}/subscriptions", payload, idempotency_key)

    def cancel_subscription(self, customer_id: str, subscription_id: str) -> dict:
        return self._request("DELETE", f"/v2/customers/{customer_id}/subscriptions/{subscription_id}")
