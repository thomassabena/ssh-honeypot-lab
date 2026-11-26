
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import asyncssh

from honeypot.events import Event, write_event


class HoneypotServer(asyncssh.SSHServer):
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.session_id = str(uuid4())

    def connection_made(self, conn: asyncssh.SSHServerConnection) -> None:
        peer = conn.get_extra_info("peername")
        source_ip, source_port = peer[:2]

        event = Event(
            timestamp=datetime.now(UTC).isoformat(),
            event_type="connection_opened",
            session_id=self.session_id,
            source_ip=source_ip,
            source_port=source_port,
        )

        write_event(event, self.log_file)


    def begin_auth(self, username: str) -> bool:
        return True

    def password_auth_supported(self) -> bool:
        return True

    
    def validate_password(self, username: str, password: str) -> bool:
        event = Event(
            timestamp=datetime.now(UTC).isoformat(),
            event_type="authentication_failed",
            session_id=self.session_id,
        )

        write_event(event, self.log_file)
        return False


    def session_requested(self) -> bool:
        return False

    def connection_requested(
        self,
        dest_host: str,
        dest_port: int,
        orig_host: str,
        orig_port: int,
    ) -> bool:
        return False


    def connection_lost(self, exc: Exception | None) -> None:
        event = Event(
            timestamp=datetime.now(UTC).isoformat(),
            event_type="connection_closed",
            session_id=self.session_id,
        )

        write_event(event, self.log_file)
