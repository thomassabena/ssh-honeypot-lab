import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Event:
    timestamp: str
    event_type: str
    session_id: str
    source_ip: str | None = None
    source_port: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)

def write_event(event: Event, log_file: Path) -> None:
    with log_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event.to_dict()) + "\n")