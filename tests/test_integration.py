import asyncio
import json

import asyncssh

from honeypot.server import HoneypotServer


def test_ssh_connection_logs_events(tmp_path):
    async def run_test():
        log_file = tmp_path / "events.jsonl"
        host_key = asyncssh.generate_private_key("ssh-ed25519")

        server = await asyncssh.create_server(
            lambda: HoneypotServer(log_file),
            "127.0.0.1",
            0,
            server_host_keys=[host_key],
        )

        try:
            port = server.get_port()

            try:
                await asyncssh.connect(
                    "127.0.0.1",
                    port=port,
                    username="testuser",
                    password="fake-password",
                    known_hosts=None,
                    client_keys=[],
                )
            except asyncssh.PermissionDenied:
                pass

            await asyncio.sleep(0.1)
        finally:
            server.close()
            await server.wait_closed()

        events = [
            json.loads(line)
            for line in log_file.read_text(encoding="utf-8").splitlines()
        ]

        event_types = [event["event_type"] for event in events]

        assert "connection_opened" in event_types
        assert "authentication_failed" in event_types
        assert "connection_closed" in event_types

    asyncio.run(run_test())
