import json

import pytest
import requests

from app import MollieError, create_app, require_test_key


def make_client(tmp_path, payments):
    """`payments` maps payment id -> dict (or callable) that the fake API returns."""
    calls = []

    def fetcher(payment_id):
        calls.append(payment_id)
        value = payments.get(payment_id)
        return value() if callable(value) else value

    app = create_app(api_key="test_dummy", fetcher=fetcher, events_file=tmp_path / "events.jsonl")
    return app.test_client(), calls, tmp_path / "events.jsonl"


def pay(status, pid="tr_abc123"):
    return {"id": pid, "status": status, "amount": {"currency": "EUR", "value": "10.00"}, "description": "Test"}


def stored(path):
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def test_paid_webhook_is_stored(tmp_path):
    client, _, events = make_client(tmp_path, {"tr_abc123": pay("paid")})
    assert client.post("/webhook", data={"id": "tr_abc123"}).status_code == 200
    assert [e["status"] for e in stored(events)] == ["paid"]


def test_duplicate_webhook_is_ignored(tmp_path):
    client, _, events = make_client(tmp_path, {"tr_abc123": pay("paid")})
    client.post("/webhook", data={"id": "tr_abc123"})
    client.post("/webhook", data={"id": "tr_abc123"})
    assert len(stored(events)) == 1


def test_status_change_is_a_new_event(tmp_path):
    state = {"status": "open"}
    client, _, events = make_client(tmp_path, {"tr_abc123": lambda: pay(state["status"])})
    client.post("/webhook", data={"id": "tr_abc123"})
    state["status"] = "paid"
    client.post("/webhook", data={"id": "tr_abc123"})
    assert [e["status"] for e in stored(events)] == ["open", "paid"]


def test_status_in_the_request_body_is_ignored(tmp_path):
    client, _, events = make_client(tmp_path, {"tr_abc123": pay("open")})
    client.post("/webhook", data={"id": "tr_abc123", "status": "paid"})
    assert [e["status"] for e in stored(events)] == ["open"]


def test_unknown_id_answers_200_and_stores_nothing(tmp_path):
    client, _, events = make_client(tmp_path, {})
    assert client.post("/webhook", data={"id": "tr_unknown1"}).status_code == 200
    assert stored(events) == []


def test_invalid_id_is_not_even_looked_up(tmp_path):
    client, calls, _ = make_client(tmp_path, {})
    for bad in ["", "abc", "../../etc/passwd", "tr_", "tr_a b c d e f"]:
        assert client.post("/webhook", data={"id": bad}).status_code == 200
    assert calls == []


@pytest.mark.parametrize("error", [MollieError(500, "boom"), requests.ConnectTimeout("slow")])
def test_api_failure_answers_500_so_mollie_retries(tmp_path, error):
    def broken():
        raise error

    client, _, events = make_client(tmp_path, {"tr_abc123": broken})
    assert client.post("/webhook", data={"id": "tr_abc123"}).status_code == 500
    assert stored(events) == []


def test_state_survives_a_restart(tmp_path):
    client, _, events = make_client(tmp_path, {"tr_abc123": pay("paid")})
    client.post("/webhook", data={"id": "tr_abc123"})
    client2, _, _ = make_client(tmp_path, {"tr_abc123": pay("paid")})
    client2.post("/webhook", data={"id": "tr_abc123"})
    assert len(stored(events)) == 1


def test_events_page_is_blocked_behind_a_tunnel(tmp_path):
    client, _, _ = make_client(tmp_path, {})
    assert client.get("/events", environ_base={"REMOTE_ADDR": "127.0.0.1"}).status_code == 200
    assert client.get("/events", headers={"X-Forwarded-For": "203.0.113.7"}, environ_base={"REMOTE_ADDR": "127.0.0.1"}).status_code == 403


def test_live_key_is_refused():
    with pytest.raises(ValueError):
        require_test_key("live_something")
    with pytest.raises(ValueError):
        require_test_key("")
