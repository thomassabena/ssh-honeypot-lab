
import asyncio
from pathlib import Path

import asyncssh

from honeypot.server import HoneypotServer


async def main():
    log_file = Path("data/events.jsonl")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    host_key = asyncssh.generate_private_key("ssh-ed25519")

    server = await asyncssh.create_server(
        lambda: HoneypotServer(log_file),
        "127.0.0.1",
        2222,
        server_host_keys=[host_key],
    )

    print("Honeypot listening on 127.0.0.1:2222")

    try:
        await asyncio.Event().wait()
    finally:
        server.close()
        await server.wait_closed()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nHoneypot stopped")
