# SSH Honeypot Experiment Lab

A lightweight SSH honeypot built in Python to observe connection attempts and experiment with different server configurations.

The project is under development. The current version provides a local SSH server, structured event logging, and automated tests.

## Features

- SSH server built with AsyncSSH
- Connection and failed authentication logging
- Unique session IDs for tracking connections
- JSONL event logs with UTC timestamps
- No real authentication, shell access, or command execution
- Unit and integration tests with pytest
- Automated checks with GitHub Actions

## Getting started

Requires Python 3.11 or later.

Clone the repository:

```bash
git clone https://github.com/thomassabena/ssh-honeypot-lab.git
cd ssh-honeypot-lab
```

Create a virtual environment and install the project:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on Linux/macOS:

```bash
source .venv/bin/activate
```

Install:

```bash
python -m pip install -e .
```

Start the server:

```bash
python -m honeypot.main
```

The server listens on `127.0.0.1:2222`.

## Testing the honeypot

From another terminal:

```bash
ssh -p 2222 testuser@127.0.0.1
```

Use a dummy password if prompted. Authentication is intentionally rejected.

The server records events in `data/events.jsonl`.

## Event logging

The current implementation records:

- `connection_opened`
- `authentication_failed`
- `connection_closed`

Each event contains a timestamp, event type, and session ID. Connection metadata is included when available.

Passwords are not stored.

## Running tests

Install the development tools:

```bash
python -m pip install pytest ruff
```

Run:

```bash
python -m pytest -v
ruff check .
```

The same checks run automatically through GitHub Actions.

## Planned work

- Configurable SSH honeypot profiles
- Reproducible local experiments
- Comparison of client interactions across profiles
- Basic experiment reporting

## Security

This project is intended for local experimentation and educational use.

The server binds to localhost by default and does not provide access to a real shell. It should not be exposed to the public Internet without additional security measures and isolation.
