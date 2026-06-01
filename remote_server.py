import csv
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

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
            # Read first 100 test cases
            for i, row in enumerate(reader):
                if i >= 100:
                    break
                TEST_CASES.append(row)
    except Exception as e:
        print(f"Error loading CSV: {e}")

@mcp.resource("test-cases://all")
def get_all_test_cases() -> str:
    """Get all 100 loaded test cases."""
    load_test_cases()
    return json.dumps(TEST_CASES, indent=2)

@mcp.tool()
def search_by_priority(priority: str) -> str:
    """Search test cases by priority. Valid values are High, Medium, Low."""
    load_test_cases()
    results = [tc for tc in TEST_CASES if tc.get('Priority', '').lower() == priority.lower()]
    return json.dumps(results, indent=2)

@mcp.tool()
def search_by_metadata(module_name: str) -> str:
    """Search test cases by metadata (Module name). Example: 'Authentication System'."""
    load_test_cases()
    results = [tc for tc in TEST_CASES if module_name.lower() in tc.get('Module', '').lower()]
    return json.dumps(results, indent=2)

@mcp.tool()
def get_test_case_by_id(test_case_id: str) -> str:
    """Get a specific test case by its ID. Example: 'TC_001'."""
    load_test_cases()
    results = [tc for tc in TEST_CASES if tc.get('Test Case ID', '').lower() == test_case_id.lower()]
    return json.dumps(results[0] if results else {"error": "Not found"}, indent=2)

if __name__ == "__main__":
    # Start the server using SSE (Server-Sent Events) for remote web connections
    # This will host the server on http://localhost:8000
    print("Starting Remote MCP Server via SSE on port 8000...")
    mcp.run(transport="sse")
