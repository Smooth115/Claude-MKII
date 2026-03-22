# Local Setup Guide

This guide covers running the Claude-MK2.5 MCP server, CLI, and Docker environment locally.

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11+ | Required for direct usage |
| pip | latest | `pip install --upgrade pip` |
| Docker + Compose | v2+ | Optional — for containerised mode |
| VS Code | latest | For MCP / Copilot Chat integration |

---

## Quick Start — Direct Python

### 1. Clone and install dependencies

```bash
git clone https://github.com/Smooth115/Claude-MK2.5.git
cd Claude-MK2.5

# MCP server
pip install -r mcp-server/requirements.txt

# CLI
pip install -r cli/requirements.txt
```

### 2. Run the CLI

```bash
# Project overview
python cli/mk2_cli.py status

# Read a file
python cli/mk2_cli.py read README.md

# Search project files
python cli/mk2_cli.py search "rootkit"

# Read all log directories
python cli/mk2_cli.py logs

# Read only the most recently modified file per directory
python cli/mk2_cli.py logs --recent

# Read a specific directory
python cli/mk2_cli.py logs evidence
```

### 3. Start the MCP server (standalone)

```bash
python mcp-server/server.py
```

The server communicates over **stdio** and is intended to be launched by a client (VS Code, the CLI `serve` command, or Docker).

---

## Quick Start — Docker

### 1. Build the image

```bash
docker compose build
```

### 2. Start the MCP server container

```bash
docker compose up mcp-server
```

### 3. Run a one-off CLI command inside Docker

```bash
docker compose run --rm cli python /project/cli/mk2_cli.py status
```

The project directory is bind-mounted into the container at `/project`, so all file tools operate against the live repository.

---

## VS Code MCP Integration

Claude-MK2.5 ships a pre-configured `.vscode/mcp.json` that defines two server entries:

| Server name | Transport | Command |
|-------------|-----------|---------|
| `claude-mk2.5` | stdio | `python mcp-server/server.py` |
| `claude-mk2.5-docker` | stdio | `docker compose run --rm -T mcp-server` |

### Enable the integration

1. Open the repository in VS Code.
2. Open the **Command Palette** (`Ctrl+Shift+P` / `Cmd+Shift+P`).
3. Run **"MCP: List Servers"** — you should see `claude-mk2.5` listed.
4. Select it and click **Start**, or VS Code may start it automatically.

> **Note:** Copilot Chat MCP support requires VS Code ≥ 1.99 with the GitHub Copilot extension.

### Available MCP tools

Once connected, the following tools are exposed to Copilot Chat:

| Tool | Description |
|------|-------------|
| `read_file` | Read any file from the project |
| `list_directory` | List contents of a directory |
| `search_files` | Full-text search across project files |
| `read_logs` | Read markdown files from log/evidence directories |
| `project_status` | Return a project structure summary |

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'mcp'`

Install dependencies:

```bash
pip install -r mcp-server/requirements.txt
```

### VS Code does not show the MCP server

- Ensure you have a recent VS Code and the GitHub Copilot extension installed.
- Check `.vscode/mcp.json` is present in the workspace root.
- Open the Output panel and select **"MCP"** to view server logs.

### Docker compose fails with `python: command not found`

The Dockerfile uses `python` (Python 3.11 image). If you see this outside Docker, use `python3` instead:

```bash
python3 mcp-server/server.py
```

### `Path escapes the project root` error

All file tool paths must be **relative** to the repository root. Use `README.md`, not `/home/user/Claude-MK2.5/README.md`.

### Docker volume permissions

If the container can't read project files, ensure the host directory is readable:

```bash
chmod -R a+r /path/to/Claude-MK2.5
```

---

## Project Structure

```
Claude-MK2.5/
├── mcp-server/
│   ├── server.py          # MCP server (FastMCP, stdio)
│   └── requirements.txt
├── cli/
│   ├── mk2_cli.py         # CLI entry point
│   └── requirements.txt
├── tools/
│   ├── parse_evtx.py      # EVTX log parser
│   ├── safe_read.py       # Safe file reader
│   └── requirements.txt
├── core/                  # Core documentation / memory files
├── evidence/              # Investigation evidence
├── logs/                  # Log files
├── investigation/         # Investigation notes
├── .vscode/
│   └── mcp.json           # VS Code MCP configuration
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```
