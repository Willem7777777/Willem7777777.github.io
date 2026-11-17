import sqlite3
from datetime import date

from mollie import MollieClient, MollieError
from studio import add_month
import pytest


def order_row(app_db, where="1=1"):
    conn = sqlite3.connect(app_db)
    conn.row_factory = sqlite3.Row
    return conn.execute(f"SELECT * FROM orders WHERE {where}").fetchall()


def join(client):
    return client.post("/join", data={"name": "Test Member", "email": "member@example.org"})


def webhook(client, payment_id):
    return client.post("/webhook", data={"id": payment_id})


# ------------------------------------------------------------------ one-off pass
def test_buy_pass_redirects_to_checkout_and_sets_webhook(client, mollie):
    response = client.post("/buy-pass")
    assert response.status_code == 303
    assert response.headers["Location"].startswith("https://checkout.example/")
    payload = mollie.created_payments[0]
    assert payload["amount"] == {"currency": "EUR", "value": "79.00"}
    assert payload["webhookUrl"] == "https://shop.example/webhook"
    assert "sequenceType" not in payload


def test_pass_becomes_paid_through_the_webhook(client, mollie, tmp_path):
    client.post("/buy-pass")
    mollie.set_status("tr_fake000001", "paid")
    assert webhook(client, "tr_fake000001").status_code == 200
    assert order_row(tmp_path / "studio.db")[0]["status"] == "paid"


def test_return_page_asks_mollie_and_does_not_trust_the_browser(client, mollie):
    client.post("/buy-pass")
    order_id = mollie.created_payments[0]["metadata"]["order_id"]
    assert b"not received" in client.get(f"/return/{order_id}?status=paid").data  # a fake query parameter changes nothing
    mollie.set_status("tr_fake000001", "paid")
    assert b"Thank you" in client.get(f"/return/{order_id}").data


# ------------------------------------------------------------------ membership and subscription
def test_join_creates_customer_and_a_first_payment(client, mollie):
    assert join(client).status_code == 303
    assert mollie.customers == [("Test Member", "member@example.org")]
    payload = mollie.created_payments[0]
    assert payload["sequenceType"] == "first"
    assert payload["customerId"] == "cst_fake0001"


def test_join_rejects_bad_input(client, mollie):
    assert client.post("/join", data={"name": "", "email": "nope"}).status_code == 400
    assert mollie.customers == []


def test_paid_first_payment_creates_one_subscription(client, mollie):
    join(client)
    mollie.set_status("tr_fake000001", "paid")
    assert webhook(client, "tr_fake000001").status_code == 200
    assert len(mollie.subscriptions) == 1
    customer_id, payload, key = mollie.subscriptions[0]
    assert customer_id == "cst_fake0001"
    assert payload["interval"] == "1 month"
    assert payload["startDate"] == add_month(date.today()).isoformat()  # first month was already paid
    assert key.startswith("studio-sub-")


def test_repeated_webhook_does_not_create_a_second_subscription(client, mollie):
    join(client)
    mollie.set_status("tr_fake000001", "paid")
    for _ in range(3):
        assert webhook(client, "tr_fake000001").status_code == 200
    assert len(mollie.subscriptions) == 1


def test_failed_first_payment_creates_no_subscription(client, mollie, tmp_path):
    join(client)
    mollie.set_status("tr_fake000001", "failed")
    webhook(client, "tr_fake000001")
    assert mollie.subscriptions == []
    assert order_row(tmp_path / "studio.db")[0]["status"] == "failed"


def test_no_mandate_yet_then_a_later_webhook_succeeds(client, mollie):
    join(client)
    mollie.set_status("tr_fake000001", "paid")
    mollie.mandates = []
    assert webhook(client, "tr_fake000001").status_code == 200
    assert mollie.subscriptions == []
    mollie.mandates = [{"id": "mdt_1", "status": "pending"}]
    assert webhook(client, "tr_fake000001").status_code == 200
    assert len(mollie.subscriptions) == 1


def test_subscription_error_gives_500_and_can_be_retried(client, mollie):
    join(client)
    mollie.set_status("tr_fake000001", "paid")
    mollie.fail_subscription = True
    assert webhook(client, "tr_fake000001").status_code == 500
    mollie.fail_subscription = False
    assert webhook(client, "tr_fake000001").status_code == 200
    assert len(mollie.subscriptions) == 1


# ------------------------------------------------------------------ webhook safety
def test_unknown_and_invalid_ids_give_200(client):
    assert webhook(client, "tr_doesnotexist").status_code == 200
    assert webhook(client, "not-an-id").status_code == 200


def test_payment_of_a_subscription_is_logged_without_an_order(client, mollie, tmp_path):
    mollie.payments["tr_monthly001"] = {"id": "tr_monthly001", "status": "paid", "amount": {"value": "49.00"}, "subscriptionId": "sub_fake0001"}
    assert webhook(client, "tr_monthly001").status_code == 200
    conn = sqlite3.connect(tmp_path / "studio.db")
    assert conn.execute("SELECT subscription_id FROM payment_log WHERE payment_id='tr_monthly001'").fetchone() == ("sub_fake0001",)


# ------------------------------------------------------------------ admin
def test_admin_is_local_only(client):
    local = {"REMOTE_ADDR": "127.0.0.1"}
    assert client.get("/admin", environ_base=local).status_code == 200
    assert client.get("/admin", headers={"X-Forwarded-For": "203.0.113.9"}, environ_base=local).status_code == 403
    assert client.get("/admin", environ_base={"REMOTE_ADDR": "203.0.113.9"}).status_code == 403


def test_cancel_subscription(client, mollie):
    join(client)
    mollie.set_status("tr_fake000001", "paid")
    webhook(client, "tr_fake000001")
    order_id = mollie.created_payments[0]["metadata"]["order_id"]
    local = {"REMOTE_ADDR": "127.0.0.1"}
    assert client.post(f"/admin/cancel/{order_id}", environ_base=local).status_code == 302
    assert mollie.cancelled == [("cst_fake0001", "sub_fake0001")]


# ------------------------------------------------------------------ helpers
@pytest.mark.parametrize("start,expected", [(date(2026, 1, 31), date(2026, 2, 28)), (date(2026, 12, 15), date(2027, 1, 15)), (date(2028, 1, 31), date(2028, 2, 29))])
def test_add_month(start, expected):
    assert add_month(start) == expected


def test_client_refuses_a_live_key():
    with pytest.raises(ValueError):
        MollieClient("live_abc")
