"""A minimal Mollie webhook receiver (test mode only).

What it does when Mollie calls POST /webhook:
  1. read the single form field `id` (for example tr_5B8cwPMGnU),
  2. fetch that payment from the Mollie API (the webhook never contains the status),
  3. log the status, and only act when the status has changed,
  4. answer 200 OK, or 500 when Mollie's API could not be reached, so that Mollie retries.

Run:  MOLLIE_API_KEY=test_... python app.py
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from flask import Flask, abort, jsonify, request

API_BASE = os.environ.get("MOLLIE_BASE_URL", "https://api.mollie.com")
PAYMENT_ID = re.compile(r"^tr_[A-Za-z0-9]{6,}$")


class MollieError(Exception):
    """The Mollie API answered with an error status."""

    def __init__(self, status: int, detail: str):
        super().__init__(f"Mollie API error {status}: {detail}")
        self.status = status


def require_test_key(key: str) -> str:
    """This project only ever talks to Mollie test mode."""
    if not key or not key.startswith("test_"):
        raise ValueError("MOLLIE_API_KEY must be set and start with test_ (test mode only).")
    return key


def fetch_payment(payment_id: str, api_key: str, base_url: str = API_BASE, timeout: float = 10):
    """Return the payment as a dict, or None when Mollie does not know the id."""
    response = requests.get(
        f"{base_url}/v2/payments/{payment_id}",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=timeout,
    )
    if response.status_code == 404:
        return None
    if response.status_code >= 400:
        raise MollieError(response.status_code, response.json().get("detail", "") if response.content else "")
    return response.json()


def _local_only() -> None:
    """Debug pages must not be reachable through a public tunnel (tunnels add X-Forwarded-For)."""
    if "X-Forwarded-For" in request.headers or request.remote_addr not in ("127.0.0.1", "::1"):
        abort(403)


def create_app(api_key: str | None = None, fetcher=None, events_file: str | Path = "events.jsonl") -> Flask:
    app = Flask(__name__)
    key = require_test_key(api_key if api_key is not None else os.environ.get("MOLLIE_API_KEY", ""))
    fetcher = fetcher or (lambda payment_id: fetch_payment(payment_id, key))
    events_path = Path(events_file)

    # Remember the last status per payment, so a repeated webhook call is recognised.
    last_status: dict[str, str] = {}
    if events_path.exists():
        for line in events_path.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            last_status[event["payment_id"]] = event["status"]

    def react(status: str, payment: dict) -> None:
        """The business logic of a shop would go here."""
        pid = payment["id"]
        if status == "paid":
            app.logger.info("%s is paid: this is the moment to ship the order or activate the service", pid)
        elif status in ("failed", "canceled", "expired"):
            app.logger.info("%s ended as %s: release the stock, maybe offer another payment method", pid, status)
        else:
            app.logger.info("%s is %s: nothing to do yet", pid, status)

    @app.post("/webhook")
    def webhook():
        payment_id = request.form.get("id", "").strip()
        if not PAYMENT_ID.match(payment_id):
            # Do not reveal anything to someone probing the URL: answer 200 and do nothing.
            app.logger.warning("webhook with an invalid id ignored")
            return "", 200
        try:
            payment = fetcher(payment_id)
        except (requests.RequestException, MollieError) as exc:
            app.logger.error("could not fetch %s: %s", payment_id, exc)
            return "", 500  # Mollie retries after a non-200 answer
        if payment is None:
            app.logger.warning("unknown payment id ignored")
            return "", 200

        status = payment["status"]  # always from the API, never from the request body
        changed = last_status.get(payment_id) != status
        if changed:
            last_status[payment_id] = status
            event = {
                "received_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "payment_id": payment_id,
                "status": status,
                "amount": payment.get("amount"),
                "description": payment.get("description"),
                "method": payment.get("method"),
                "sequence_type": payment.get("sequenceType"),
                "subscription_id": payment.get("subscriptionId"),
                "metadata": payment.get("metadata"),
            }
            with events_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event) + "\n")
            react(status, payment)
        else:
            app.logger.info("duplicate webhook for %s (still %s): ignored", payment_id, status)
        return "", 200

    @app.get("/events")
    def events():
        _local_only()
        if not events_path.exists():
            return jsonify([])
        lines = events_path.read_text(encoding="utf-8").splitlines()[-50:]
        return jsonify([json.loads(line) for line in lines])

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    return app


if __name__ == "__main__":
    import logging

    try:  # optional: read MOLLIE_API_KEY from a local .env file
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass
    logging.basicConfig(level=logging.INFO)
    create_app().run(port=int(os.environ.get("PORT", "5000")))
