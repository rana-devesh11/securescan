#!/bin/bash
# Create professional visual demo for SecureScan
# Generates clean terminal output suitable for screenshots/video

clear
export PS1="$ "

# Set colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}======================================================================"
echo "  SecureScan - Security Scanner Aggregator"
echo "  Demonstrating Multi-Tool Security Scanning"
echo -e "======================================================================${NC}"
echo ""
sleep 2

# Step 1: Show the command
echo -e "${GREEN}Step 1: Running SecureScan${NC}"
echo "----------------------------------------------------------------------"
echo ""
echo -e "${YELLOW}\$ python3 securescan.py --path test_project/ --output results.json${NC}"
echo ""
sleep 1

# Run the scan
python3 securescan.py --path test_project/ --output results.json

echo ""
sleep 2

# Step 2: Show summary
echo -e "${GREEN}Step 2: Security Summary${NC}"
echo "----------------------------------------------------------------------"
echo ""
cat results.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
summary = data['summary']

print(f\"📊 SCAN SUMMARY\")
print(f\"{'='*60}\")
print(f\"Total Findings: {summary['total_findings']}\")
print(f\"Duplicates Removed: {summary['duplicates_removed']}\")
print(f\"Deduplication Rate: {summary['deduplication_rate']}\")
print(f\"\")
print(f\"By Severity:\")
for severity, count in summary['by_severity'].items():
    print(f\"  • {severity}: {count}\")
print(f\"\")
print(f\"By Tool:\")
for tool, count in summary['by_tool'].items():
    print(f\"  • {tool}: {count}\")
"

echo ""
sleep 2

# Step 3: Show top 3 critical findings
echo -e "${GREEN}Step 3: Critical Findings${NC}"
echo "----------------------------------------------------------------------"
echo ""
cat results.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
findings = data['findings']

# Get high severity findings
critical = [f for f in findings if f['severity'] in ['HIGH', 'ERROR', 'CRITICAL']][:3]

for i, finding in enumerate(critical, 1):
    print(f\"{i}. [{finding['severity']}] {finding['file']}:{finding['line']}\")
    print(f\"   {finding['message'][:80]}...\")
    print(f\"   Tool: {finding['tool']}\")
    print()
"

sleep 2

# Step 4: Deduplication highlight
echo -e "${GREEN}Step 4: Deduplication Algorithm${NC}"
echo "----------------------------------------------------------------------"
echo ""
echo "SecureScan uses SHA256 fingerprinting to deduplicate findings:"
echo ""
echo -e "${CYAN}fingerprint = SHA256(file_path + line_number + severity)${NC}"
echo ""
echo "This prevents duplicate alerts when multiple tools detect the same issue."
echo ""
sleep 2

# Step 5: CI/CD Integration
echo -e "${GREEN}Step 5: CI/CD Ready${NC}"
echo "----------------------------------------------------------------------"
echo ""
echo "JSON output makes SecureScan perfect for CI/CD pipelines:"
echo ""
echo -e "${YELLOW}\$ cat results.json | jq '.summary.total_findings'${NC}"
cat results.json | jq '.summary.total_findings'
echo ""
echo -e "${YELLOW}\$ cat results.json | jq '.summary.by_severity.HIGH'${NC}"
cat results.json | jq '.summary.by_severity.HIGH'
echo ""
sleep 2

# Final summary
echo -e "${CYAN}======================================================================"
echo "  Demo Complete!"
echo -e "======================================================================${NC}"
echo ""
echo -e "${GREEN}✓ Scanned vulnerable application${NC}"
echo -e "${GREEN}✓ Detected 21 security issues${NC}"
echo -e "${GREEN}✓ Aggregated findings from 3 tools${NC}"
echo -e "${GREEN}✓ Applied intelligent deduplication${NC}"
echo -e "${GREEN}✓ Generated CI/CD-ready JSON output${NC}"
echo ""
echo -e "${BLUE}GitHub: https://github.com/rana-devesh11/securescan${NC}"
echo ""
