import pytest

from mollie import MollieError
from studio import create_app


class FakeMollie:
    """Stands in for the Mollie API so the tests run offline."""

    def __init__(self):
        self.payments = {}          # id -> payment dict returned by get_payment
        self.created_payments = []
        self.customers = []
        self.mandates = [{"id": "mdt_1", "status": "valid"}]
        self.subscriptions = []     # (customer_id, payload, idempotency_key)
        self.cancelled = []
        self.fail_subscription = False
        self._n = 0

    def create_customer(self, name, email):
        self.customers.append((name, email))
        return {"id": "cst_fake0001"}

    def create_payment(self, payload, idempotency_key=None):
        self._n += 1
        pid = f"tr_fake{self._n:06d}"
        self.created_payments.append(payload)
        self.payments[pid] = {"id": pid, "status": "open", "amount": payload["amount"], "metadata": payload.get("metadata")}
        return {"id": pid, "_links": {"checkout": {"href": f"https://checkout.example/{pid}"}}}

    def get_payment(self, payment_id):
        if payment_id not in self.payments:
            raise MollieError(404, "not found")
        return self.payments[payment_id]

    def list_mandates(self, customer_id):
        return self.mandates

    def create_subscription(self, customer_id, payload, idempotency_key=None):
        if self.fail_subscription:
            raise MollieError(500, "boom")
        self.subscriptions.append((customer_id, payload, idempotency_key))
        return {"id": f"sub_fake{len(self.subscriptions):04d}"}

    def cancel_subscription(self, customer_id, subscription_id):
        self.cancelled.append((customer_id, subscription_id))
        return {"status": "canceled"}

    def set_status(self, payment_id, status):
        self.payments[payment_id]["status"] = status


@pytest.fixture
def mollie():
    return FakeMollie()


@pytest.fixture
def app(mollie, tmp_path):
    return create_app(mollie, tmp_path / "studio.db", public_url="https://shop.example")


@pytest.fixture
def client(app):
    return app.test_client()
