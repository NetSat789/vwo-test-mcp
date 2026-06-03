import csv
from pathlib import Path
from collections import defaultdict

csv_path = Path('vwo_login_test_cases.csv')
with open(csv_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    test_cases = list(reader)

# Count by priority
priority_count = defaultdict(int)
critical_tests = []

for tc in test_cases:
    priority = tc.get('Priority', '').strip()
    priority_count[priority] += 1
    if priority.lower() == 'critical':
        critical_tests.append(tc)

# Summary
print("=" * 80)
print("TEST CASES SUMMARY FROM MCP REMOTE DEPLOY")
print("=" * 80)
print(f"\nTotal Test Cases: {len(test_cases)}")
print("\nPriority Distribution:")
for priority in sorted(priority_count.keys(), key=lambda x: priority_count[x], reverse=True):
    print(f"  {priority}: {priority_count[priority]}")

print(f"\n{'=' * 80}")
print(f"CRITICAL PRIORITY TEST CASES ({len(critical_tests)} total)")
print("=" * 80)
for tc in critical_tests:
    print(f"\n{tc['Test Case ID']}: {tc['Test Case Description']}")
    print(f"  Module: {tc['Module']}")
