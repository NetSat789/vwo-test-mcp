# vwo-test-mcp

A **remote MCP (Model Context Protocol) server** deployed on [Render](https://render.com) that exposes **500 VWO Login Page test cases** to any AI coding assistant (Claude, Cline, Antigravity, etc.) via a simple config.

> ⚠️ **Private Project** — Server URL and connection details are shared privately. Contact the repo owner to get access.

---

## 🛠️ Available Tools

Once connected, the following MCP tools are available:

| Tool | Description | Parameters |
|---|---|---|
| `list_test_cases` | List test cases with pagination | `limit` (default: 50), `offset` (default: 0) |
| `get_test_case_by_id` | Fetch a specific test case | `test_case_id` (e.g. `TC_001`) |
| `search_by_priority` | Filter by priority level | `priority`: `High`, `Medium`, or `Low` |
| `search_by_module` | Filter by module name | `module` (e.g. `Login`) |

### Example Usage in AI Chat

```
"List 10 High priority test cases for VWO login"
"Get test case TC_042"
"Show all test cases for the Login module"
```

---

## 📁 Project Structure

```
vwo-test-mcp/
├── remote_server.py          # FastMCP SSE server with all tools
├── vwo_login_test_cases.csv  # 500 VWO login test cases dataset
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 🏗️ Architecture

```
AI Client (Cline / Antigravity / Claude)
        │
        │  stdio (JSON-RPC)
        ▼
  supergateway (npx)           ← universal SSE-to-stdio bridge
        │
        │  HTTPS / SSE
        ▼
  Render Cloud                 ← FastMCP + Uvicorn
        │
        │  reads
        ▼
  vwo_login_test_cases.csv     ← 500 test cases
```

---

## 🧱 Server Tech Stack

| Component | Technology |
|---|---|
| MCP Framework | [FastMCP](https://github.com/jlowin/fastmcp) (`mcp[cli] >= 1.0.0`) |
| Web Server | Uvicorn + Starlette (ASGI) |
| Transport | SSE (Server-Sent Events) |
| Hosting | [Render](https://render.com) |
| Data | CSV — 500 VWO login test cases |

---

## ⚙️ Server Setup (for self-hosting)

If you want to run your own instance:

### Prerequisites
- Python 3.10+
- A [Render](https://render.com) account (or any cloud that runs Python)
- Node.js (for the `npx supergateway` client connector)

### Local Development

```bash
git clone https://github.com/NetSat789/vwo-test-mcp.git
cd vwo-test-mcp
pip install -r requirements.txt
python remote_server.py
```

Server runs at `http://localhost:8000/sse`.

### Deploy on Render

1. Fork this repo.
2. Create a new **Web Service** on Render pointing to your fork.
3. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python remote_server.py`
4. Render auto-assigns the `PORT` environment variable — the server reads it automatically.
5. Use your own Render URL in the client config above.

---

## 📋 Test Case Dataset

The dataset (`vwo_login_test_cases.csv`) contains **500 test cases** for the VWO Login page covering:

| Module | Priority Levels |
|---|---|
| Login | High, Medium, Low |
| Password Reset | High, Medium |
| SSO / OAuth | High, Medium, Low |
| Error Handling | High, Medium, Low |
| Session Management | Medium, Low |
| UI / Accessibility | Low |

**CSV Columns:** `Test Case ID`, `Module`, `Priority`, `Test Case Title`, `Preconditions`, `Test Steps`, `Expected Result`

---

## 🐛 Troubleshooting

### `Method Not Allowed` error
This happens when the MCP client does not correctly handle SSE relative URLs. Using `npx supergateway` as the client connector fixes this completely.

**Root cause:** Some older MCP clients had a bug where they ignored the SSE `endpoint` event and sent `POST` requests directly to `/sse` (which only accepts `GET`).

**Fix applied to server:** A `RootPathMiddleware` was added that forces the server to emit **absolute URLs** in the SSE endpoint event. This makes the server compatible with both buggy and compliant clients.

### Slow first connection
Render free tier spins down after inactivity. The first connection may take **30–60 seconds** while the server wakes up. Subsequent requests are fast.

### `npx` not found
Install [Node.js](https://nodejs.org/en/download) — `npx` is bundled with it.

---

## 📅 Changelog

### 2026-06-03
- **Fixed universal client compatibility** — replaced hardcoded Python proxy script with `npx supergateway`. Now works on any OS with Node.js installed.
- **Fixed `Method Not Allowed` error** — added `RootPathMiddleware` and URL encoding patch to emit absolute SSE endpoint URLs.
- **Added `RootPathMiddleware`** — reads `X-Forwarded-Proto` and `Host` headers from Render/Cloudflare to construct correct absolute callback URLs.
- **Added CORS middleware** — allows connections from any origin.

### 2026-06-01 — 2026-06-02
- **Initial deployment on Render** — FastMCP server deployed with SSE transport.
- **Added 4 MCP tools** — `list_test_cases`, `get_test_case_by_id`, `search_by_priority`, `search_by_module`.
- **Added pagination** — `list_test_cases` supports `limit` and `offset` parameters to avoid token overload.
- **Fixed `421 Misdirected Request`** — configured Uvicorn with `proxy_headers=True` and `forwarded_allow_ips="*"` to correctly handle Cloudflare/Render reverse proxy headers.
- **Loaded 500 test cases** from CSV into memory at startup for fast in-memory querying.

### 2026-05-27
- **Generated 500 VWO login test cases** from a test plan document into `vwo_login_test_cases.csv`.

---

## 📄 License

MIT
