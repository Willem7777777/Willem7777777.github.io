"""Lotus Yoga Studio: a small proof of concept for a fictional merchant (test mode only).

The studio sells two things:
  * a 10-class pass, paid once (a normal payment), and
  * a monthly membership: the first payment creates a mandate, after which a subscription charges the member monthly.

Everything that matters happens in the webhook, not on the page the customer returns to.
"""
from __future__ import annotations

import calendar
import os
import re
import sqlite3
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

from flask import Flask, abort, redirect, render_template_string, request, url_for

from mollie import MollieClient, MollieError

PASS_PRICE = "79.00"
MEMBERSHIP_PRICE = "49.00"
PAYMENT_ID = re.compile(r"^tr_[A-Za-z0-9]{6,}$")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY, kind TEXT NOT NULL, name TEXT, email TEXT,
    payment_id TEXT, customer_id TEXT, status TEXT NOT NULL,
    sub_state TEXT, subscription_id TEXT, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS payment_log (
    payment_id TEXT PRIMARY KEY, status TEXT NOT NULL, subscription_id TEXT, amount TEXT, seen_at TEXT NOT NULL
);
"""


def add_month(day: date) -> date:
    """One month later; if that day does not exist (31 January) use the last day of the month."""
    year, month = day.year + day.month // 12, day.month % 12 + 1
    return date(year, month, min(day.day, calendar.monthrange(year, month)[1]))


def money(value: str) -> dict:
    return {"currency": "EUR", "value": value}


PAGE = """<!doctype html><title>Lotus Yoga Studio (demo)</title>
<style>body{font-family:system-ui,sans-serif;max-width:640px;margin:40px auto;padding:0 16px;line-height:1.5}
.box{border:1px solid #ddd;border-radius:8px;padding:16px;margin:16px 0}input,button{font:inherit;padding:6px 10px;margin:4px 0}
.note{color:#666;font-size:.9rem}</style>
<h1>Lotus Yoga Studio</h1><p class="note">Demo with the Mollie <b>test</b> environment. No real money, no real data.</p>
{{ body|safe }}"""


def create_app(mollie, db_path: str | Path = "studio.db", public_url: str = "http://localhost:5000") -> Flask:
    app = Flask(__name__)
    db_file = str(db_path)

    def db() -> sqlite3.Connection:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        return conn

    with db() as conn:
        conn.executescript(SCHEMA)

    def local_only() -> None:
        """Admin pages must not be reachable through a public tunnel (tunnels add X-Forwarded-For)."""
        if "X-Forwarded-For" in request.headers or request.remote_addr not in ("127.0.0.1", "::1"):
            abort(403)

    def render(body: str) -> str:
        return render_template_string(PAGE, body=body)

    # ------------------------------------------------------------------ pages
    @app.get("/")
    def home():
        return render(
            f"""
<div class="box"><h2>10-class pass: EUR {PASS_PRICE}</h2><p>Pay once. Valid for ten classes.</p>
<form method="post" action="{url_for('buy_pass')}"><button>Buy the pass</button></form></div>
<div class="box"><h2>Monthly membership: EUR {MEMBERSHIP_PRICE} per month</h2>
<p>The first month is paid now. After that we charge you automatically every month, until you cancel.</p>
<form method="post" action="{url_for('join')}">
<input name="name" placeholder="Name" required><br><input name="email" type="email" placeholder="Email" required><br>
<button>Become a member</button></form></div>"""
        )

    @app.post("/buy-pass")
    def buy_pass():
        order_id = uuid.uuid4().hex[:10]
        payment = mollie.create_payment(
            {
                "amount": money(PASS_PRICE),
                "description": f"Lotus Yoga 10-class pass {order_id}",
                "redirectUrl": f"{public_url}/return/{order_id}",
                "webhookUrl": f"{public_url}/webhook",
                "metadata": {"order_id": order_id, "kind": "pass"},
            },
            idempotency_key=f"studio-pass-{order_id}",
        )
        with db() as conn:
            conn.execute(
                "INSERT INTO orders (id, kind, payment_id, status, created_at) VALUES (?, 'pass', ?, 'open', ?)",
                (order_id, payment["id"], datetime.now(timezone.utc).isoformat(timespec="seconds")),
            )
        return redirect(payment["_links"]["checkout"]["href"], 303)

    @app.post("/join")
    def join():
        name, email = request.form.get("name", "").strip(), request.form.get("email", "").strip()
        if not name or not EMAIL.match(email):
            return render("<p>Please enter a name and a valid email address.</p><p><a href='/'>Back</a></p>"), 400
        order_id = uuid.uuid4().hex[:10]
        customer = mollie.create_customer(name, email)
        payment = mollie.create_payment(
            {
                "amount": money(MEMBERSHIP_PRICE),
                "description": f"Lotus Yoga membership, first month {order_id}",
                "redirectUrl": f"{public_url}/return/{order_id}",
                "webhookUrl": f"{public_url}/webhook",
                "customerId": customer["id"],
                "sequenceType": "first",  # this payment asks the customer's permission for later charges (a mandate)
                "metadata": {"order_id": order_id, "kind": "membership"},
            },
            idempotency_key=f"studio-first-{order_id}",
        )
        with db() as conn:
            conn.execute(
                "INSERT INTO orders (id, kind, name, email, payment_id, customer_id, status, created_at)"
                " VALUES (?, 'membership', ?, ?, ?, ?, 'open', ?)",
                (order_id, name, email, payment["id"], customer["id"], datetime.now(timezone.utc).isoformat(timespec="seconds")),
            )
        return redirect(payment["_links"]["checkout"]["href"], 303)

    @app.get("/return/<order_id>")
    def return_page(order_id: str):
        with db() as conn:
            order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if order is None:
            abort(404)
        # Ask Mollie instead of trusting the browser. The webhook is still the source of truth for our own records.
        try:
            status = mollie.get_payment(order["payment_id"])["status"]
        except MollieError:
            status = order["status"]
        messages = {
            "paid": "Thank you! Your payment was received.",
            "open": "We have not received your payment yet. If you already paid, this page may be a few seconds ahead of the bank.",
            "pending": "Your payment is being processed.",
            "failed": "The payment failed. You were not charged. Please try again.",
            "canceled": "You canceled the payment. You were not charged.",
            "expired": "The payment link expired. Please start again.",
        }
        return render(f"<h2>Order {order_id}</h2><p>{messages.get(status, 'Status: ' + status)}</p><p><a href='/'>Back</a></p>")

    # ---------------------------------------------------------------- webhook
    @app.post("/webhook")
    def webhook():
        payment_id = request.form.get("id", "").strip()
        if not PAYMENT_ID.match(payment_id):
            return "", 200  # nothing to learn for someone probing the URL
        try:
            payment = mollie.get_payment(payment_id)
        except MollieError as exc:
            if exc.status == 404:
                return "", 200
            return "", 500  # Mollie will retry
        except Exception:  # network problems
            return "", 500

        status = payment["status"]
        with db() as conn:
            conn.execute(
                "INSERT INTO payment_log (payment_id, status, subscription_id, amount, seen_at) VALUES (?, ?, ?, ?, ?)"
                " ON CONFLICT(payment_id) DO UPDATE SET status = excluded.status, seen_at = excluded.seen_at",
                (payment_id, status, payment.get("subscriptionId"), (payment.get("amount") or {}).get("value"),
                 datetime.now(timezone.utc).isoformat(timespec="seconds")),
            )
            order = conn.execute("SELECT * FROM orders WHERE payment_id = ?", (payment_id,)).fetchone()
            if order is None:
                # For example a monthly subscription payment: new to us, but it carries the subscription id.
                return "", 200
            conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order["id"]))

        if order["kind"] == "membership" and status == "paid":
            return start_subscription(order)
        return "", 200

    def start_subscription(order):
        """Create the monthly subscription exactly once, after the first payment succeeded."""
        # Claim the job first. A second webhook call arriving now finds the claim and does nothing.
        with db() as conn:
            claimed = conn.execute(
                "UPDATE orders SET sub_state = 'creating' WHERE id = ? AND sub_state IS NULL", (order["id"],)
            ).rowcount
        if not claimed:
            return "", 200

        def release() -> None:
            with db() as conn:
                conn.execute("UPDATE orders SET sub_state = NULL WHERE id = ?", (order["id"],))

        try:
            mandates = mollie.list_mandates(order["customer_id"])
            if not any(m["status"] in ("valid", "pending") for m in mandates):
                release()  # the mandate may still be on its way; a later webhook call tries again
                app.logger.warning("order %s is paid but there is no usable mandate yet", order["id"])
                return "", 200
            subscription = mollie.create_subscription(
                order["customer_id"],
                {
                    "amount": money(MEMBERSHIP_PRICE),
                    "interval": "1 month",
                    "startDate": add_month(date.today()).isoformat(),  # the first month was just paid
                    "description": f"Lotus Yoga membership {order['id']}",
                    "webhookUrl": f"{public_url}/webhook",
                    "metadata": {"order_id": order["id"]},
                },
                idempotency_key=f"studio-sub-{order['id']}",  # protects against a double charge if we retry
            )
        except Exception as exc:
            release()
            app.logger.error("could not create subscription for order %s: %s", order["id"], exc)
            return "", 500
        with db() as conn:
            conn.execute(
                "UPDATE orders SET subscription_id = ?, sub_state = 'done' WHERE id = ?", (subscription["id"], order["id"])
            )
        return "", 200

    # ------------------------------------------------------------------ admin
    @app.get("/admin")
    def admin():
        local_only()
        with db() as conn:
            orders = conn.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()
        rows = "".join(
            f"<tr><td>{o['id']}</td><td>{o['kind']}</td><td>{o['status']}</td><td>{o['subscription_id'] or ''}</td>"
            + (
                f"<td><form method='post' action='{url_for('cancel', order_id=o['id'])}'><button>Cancel</button></form></td>"
                if o["subscription_id"]
                else "<td></td>"
            )
            + "</tr>"
            for o in orders
        )
        return render(f"<h2>Orders (local only)</h2><table border=1 cellpadding=6><tr><th>Order</th><th>Kind</th><th>Status</th><th>Subscription</th><th></th></tr>{rows}</table>")

    @app.post("/admin/cancel/<order_id>")
    def cancel(order_id: str):
        local_only()
        with db() as conn:
            order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if order is None or not order["subscription_id"]:
            abort(404)
        mollie.cancel_subscription(order["customer_id"], order["subscription_id"])
        with db() as conn:
            conn.execute("UPDATE orders SET subscription_id = NULL, sub_state = 'canceled' WHERE id = ?", (order_id,))
        return redirect(url_for("admin"))

    return app


if __name__ == "__main__":
    import logging

    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass
    logging.basicConfig(level=logging.INFO)
    port = int(os.environ.get("PORT", "5000"))
    create_app(
        MollieClient(os.environ.get("MOLLIE_API_KEY", "")),
        public_url=os.environ.get("PUBLIC_URL", f"http://localhost:{port}"),
    ).run(port=port)
