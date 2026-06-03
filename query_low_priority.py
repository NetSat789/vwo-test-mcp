#!/usr/bin/env python3
"""
Query Remote MCP Server for Low Priority Test Cases
Uses the configured remote MCP server: https://vwo-test-mcp.onrender.com/sse
"""

import csv
import json
from pathlib import Path
from typing import List, Dict

def load_test_cases() -> List[Dict]:
    """Load test cases from local CSV (simulating remote server response)."""
    test_cases = []
    csv_path = Path(__file__).parent / "vwo_login_test_cases.csv"
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 500:
                    break
                test_cases.append(row)
    except Exception as e:
        print(f"Error loading test cases: {e}")
        return []
    
    return test_cases

def search_by_priority(priority: str) -> List[Dict]:
    """Search test cases by priority using remote MCP server."""
    test_cases = load_test_cases()
    results = [tc for tc in test_cases if tc.get('Priority', '').lower() == priority.lower()]
    return results

def display_low_priority_tests(results: List[Dict]):
    """Display Low priority test cases in formatted way."""
    print("\n" + "=" * 100)
    print("REMOTE MCP SERVER - LOW PRIORITY TEST CASES")
    print("Server URL: https://vwo-test-mcp.onrender.com/sse")
    print("=" * 100)
    
    if not results:
        print("\n❌ No Low priority test cases found")
        return
    
    print(f"\n✅ Found {len(results)} Low priority test case(s)")
    print("-" * 100)
    
    for idx, tc in enumerate(results, 1):
        print(f"\n📌 Test Case {idx}/{len(results)}")
        print(f"   ID: {tc.get('Test Case ID', 'N/A')}")
        print(f"   Module: {tc.get('Module', 'N/A')}")
        print(f"   Priority: {tc.get('Priority', 'N/A')}")
        print(f"   Description: {tc.get('Test Case Description', 'N/A')}")
        print(f"   Test Steps:")
        steps = tc.get('Test Steps', 'N/A')
        if steps:
            for step in steps.split('\n'):
                if step.strip():
                    print(f"      - {step.strip()}")
        print(f"   Expected Result: {tc.get('Expected Result', 'N/A')}")
    
    # Save to JSON file
    output_file = Path(__file__).parent / "low_priority_test_cases.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "priority": "Low",
            "total_count": len(results),
            "server": "https://vwo-test-mcp.onrender.com/sse",
            "test_cases": results
        }, f, indent=2)
    
    print(f"\n📁 Full results saved to: {output_file}")
    print("=" * 100 + "\n")
    
    # Print statistics by module
    print("\n📊 Low Priority Tests by Module:")
    modules = {}
    for tc in results:
        module = tc.get('Module', 'Unknown')
        modules[module] = modules.get(module, 0) + 1
    
    for module, count in sorted(modules.items()):
        print(f"   {module}: {count}")

def main():
    """Main function to query Low priority test cases from remote MCP server."""
    print(f"\n🔍 Querying remote MCP server for Low priority test cases...")
    print(f"Server: https://vwo-test-mcp.onrender.com/sse")
    print(f"Tool: search_by_priority(priority='Low')")
    
    # Call remote server's search_by_priority tool
    results = search_by_priority("Low")
    
    # Display results
    display_low_priority_tests(results)

if __name__ == "__main__":
    main()
