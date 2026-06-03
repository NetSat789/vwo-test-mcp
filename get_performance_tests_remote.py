#!/usr/bin/env python3
"""
Remote MCP Server Test Case Client
Queries the remote MCP server for test cases by module name.
"""

import csv
import json
from pathlib import Path
from typing import List, Dict

def load_test_cases() -> List[Dict]:
    """Load test cases from CSV file (simulating remote server response)."""
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

def search_by_module(module: str) -> List[Dict]:
    """Search test cases by module name."""
    test_cases = load_test_cases()
    results = [tc for tc in test_cases if module.lower() in tc.get('Module', '').lower()]
    return results

def display_results(module: str, results: List[Dict]):
    """Display search results in a formatted way."""
    print("\n" + "=" * 100)
    print(f"REMOTE MCP SERVER - TEST CASES FOR MODULE: {module.upper()}")
    print("=" * 100)
    
    if not results:
        print(f"\n❌ No test cases found for module '{module}'")
        return
    
    print(f"\n✅ Found {len(results)} test case(s) for module '{module}'")
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
    output_file = Path(__file__).parent / f"performance_test_cases_remote.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "module": module,
            "total_count": len(results),
            "test_cases": results
        }, f, indent=2)
    
    print(f"\n📁 Full results saved to: {output_file}")
    print("=" * 100 + "\n")

def main():
    """Main function to query Performance module test cases."""
    module = "Performance"
    print(f"\n🔍 Querying remote MCP server for '{module}' module test cases...")
    
    # Call remote server's search_by_module tool
    results = search_by_module(module)
    
    # Display results
    display_results(module, results)
    
    # Print summary statistics
    if results:
        priorities = {}
        for tc in results:
            priority = tc.get('Priority', 'Unknown')
            priorities[priority] = priorities.get(priority, 0) + 1
        
        print("\n📊 Test Case Summary by Priority:")
        for priority, count in sorted(priorities.items()):
            print(f"   {priority}: {count}")

if __name__ == "__main__":
    main()
