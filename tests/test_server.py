import json
from unittest.mock import MagicMock

from honeypot.server import HoneypotServer


def test_connection_made_logs_event(tmp_path):
    log_file = tmp_path / "events.jsonl"

    # Simulate an incoming SSH connection
    connection = MagicMock()
    connection.get_extra_info.return_value = ("127.0.0.1", 54321)

    server = HoneypotServer(log_file)
    server.connection_made(connection)

    # Read the recorded event
    with log_file.open("r", encoding="utf-8") as file:
        event = json.loads(file.readline())

    assert event["event_type"] == "connection_opened"
    assert event["source_ip"] == "127.0.0.1"
    assert event["source_port"] == 54321
    assert event["session_id"]


def test_unique_session_ids(tmp_path):
    log_file = tmp_path / "events.jsonl"

    server1 = HoneypotServer(log_file)
    server2 = HoneypotServer(log_file)

    assert server1.session_id != server2.session_id



def test_failed_authentication_is_logged(tmp_path):
    log_file = tmp_path / "events.jsonl"
    server = HoneypotServer(log_file)

    result = server.validate_password("testuser", "fake-password")

    with log_file.open("r", encoding="utf-8") as file:
        event = json.loads(file.readline())

    assert result is False
    assert event["event_type"] == "authentication_failed"
    assert event["session_id"] == server.session_id

    # Passwords must never appear in logs
    assert "fake-password" not in log_file.read_text(encoding="utf-8")


def test_connection_closed_is_logged(tmp_path):
    log_file = tmp_path / "events.jsonl"
    server = HoneypotServer(log_file)

    server.connection_lost(None)

    with log_file.open("r", encoding="utf-8") as file:
        event = json.loads(file.readline())

    assert event["event_type"] == "connection_closed"
    assert event["session_id"] == server.session_id

