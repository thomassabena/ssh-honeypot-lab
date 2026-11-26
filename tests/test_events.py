import json

from honeypot.events import Event, write_event


def test_event_serialization():
    event = Event(
        timestamp="2026-11-26T15:00:00Z",
        event_type="connection_opened",
        session_id="abc123",
    )

    result = event.to_dict()

    assert result["timestamp"] == "2026-11-26T15:00:00Z"
    assert result["event_type"] == "connection_opened"
    assert result["session_id"] == "abc123"

def test_event_with_optional_fields():
    event = Event(
        timestamp="2026-11-26T15:00:00Z",
        event_type="connection_opened",
        session_id="abc123",
        source_ip="127.0.0.1",
        source_port=54321,
    )

    result = event.to_dict()

    assert result["source_ip"] == "127.0.0.1"
    assert result["source_port"] == 54321

def test_write_event(tmp_path):
    log_file = tmp_path / "events.jsonl"

    event = Event(
        timestamp="2026-11-26T15:00:00Z",
        event_type="connection_opened",
        session_id="abc123",
    )

    write_event(event, log_file)

    with log_file.open("r", encoding="utf-8") as file:
        data = json.loads(file.readline())

    assert data == event.to_dict()


def test_write_multiple_events(tmp_path):
    log_file = tmp_path / "events.jsonl"

    for i in range(3):
        event = Event(
            timestamp="2026-11-26T15:00:00Z",
            event_type="connection_opened",
            session_id=f"session-{i}",
        )
        write_event(event, log_file)

    with log_file.open("r", encoding="utf-8") as file:
        events = [json.loads(line) for line in file]

    assert len(events) == 3
    assert [event["session_id"] for event in events] == [
        "session-0",
        "session-1",
        "session-2",
    ]
