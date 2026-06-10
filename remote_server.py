import os
import csv
import json
import uvicorn
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# Initialize FastMCP server specifically for remote (SSE) usage
mcp = FastMCP("TestCaseRemoteMCP")

# Global variable to store test cases
TEST_CASES = []

def load_test_cases():
    global TEST_CASES
    if TEST_CASES:
        return
    
    csv_path = Path(__file__).parent / "vwo_login_test_cases.csv"
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Read all test cases
            for row in reader:
                TEST_CASES.append(row)
    except Exception as e:
        print(f"Error loading CSV: {e}")

@mcp.resource("test-cases://all")
def get_all_test_cases() -> str:
    """Get all loaded test cases."""
    load_test_cases()
    return json.dumps(TEST_CASES, indent=2)

@mcp.tool()
def search_by_priority(priority: str) -> str:
    """Search test cases by priority. Valid values are High, Medium, Low."""
    load_test_cases()
    results = [tc for tc in TEST_CASES if tc.get('Priority', '').lower() == priority.lower()]
    return json.dumps(results, indent=2)




@mcp.tool()
def get_test_case_by_id(test_case_id: str) -> str:
    """Get a specific test case by its ID. Example: 'TC_001'."""
    load_test_cases()
    results = [tc for tc in TEST_CASES if tc.get('Test Case ID', '').lower() == test_case_id.lower()]
    return json.dumps(results[0] if results else {"error": "Not found"}, indent=2)

@mcp.tool()
def list_test_cases(
    limit: int = Field(50, description="Number of test cases to return"), 
    offset: int = Field(0, description="The starting index for pagination")
) -> str:
    """List test cases with pagination."""
    load_test_cases()
    results = TEST_CASES[offset : offset + limit]
    return json.dumps(results, indent=2)

@mcp.tool()
def search_by_module(module: str) -> str:
    """Search test cases strictly by Module name."""
    load_test_cases()
    results = [tc for tc in TEST_CASES if module.lower() in tc.get('Module', '').lower()]
    return json.dumps(results, indent=2)

@mcp.tool()
def get_test_cases_by_range(
    start_index: int = Field(0, description="start index"),
    end_index: int = Field(50, description="end index")
) -> str:
    """Get test cases by index range. Example: start_index=500, end_index=550."""
    load_test_cases()
    if start_index < 0 or end_index > len(TEST_CASES) or start_index >= end_index:
        return json.dumps({"error": f"Invalid range. Total test cases: {len(TEST_CASES)}"}, indent=2)
    results = TEST_CASES[start_index:end_index]
    return json.dumps({"total_in_range": len(results), "test_cases": results}, indent=2)


from starlette.middleware.cors import CORSMiddleware

# --- BEGIN MONKEY PATCH FOR ABSOLUTE URLS ---
# This fixes the "Method Not Allowed" error for MCP clients that do not support
# relative URLs in the SSE endpoint event by forcing an absolute URL.
import mcp.server.sse as mcp_sse
import urllib.parse
original_quote = urllib.parse.quote

def custom_quote(string, safe='/', encoding=None, errors=None):
    return original_quote(string, safe=safe + ':', encoding=encoding, errors=errors)

mcp_sse.quote = custom_quote

class RootPathMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] in ("http", "websocket"):
            headers = dict(scope.get("headers", []))
            host = headers.get(b"host", b"").decode("utf-8")
            proto = headers.get(b"x-forwarded-proto", b"http").decode("utf-8")
            if host:
                scope["root_path"] = f"{proto}://{host}"
        await self.app(scope, receive, send)
# --- END MONKEY PATCH ---

# Extract the Starlette ASGI web application
app = mcp.sse_app()
app.add_middleware(RootPathMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # Render assigns a dynamic PORT environment variable. We use 8000 as a fallback.
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Remote MCP Server via SSE on port {port}...")
    
    # Run the server using uvicorn so we can specify the exact host and port
    uvicorn.run(app, host="0.0.0.0", port=port, proxy_headers=True, forwarded_allow_ips="*")
