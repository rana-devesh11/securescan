#!/bin/bash
# SecureScan Demo Recording Script
# Creates terminal recording showing SecureScan in action

set -e

echo "======================================================================"
echo "  SecureScan Demo - Recording Terminal Session"
echo "======================================================================"
echo ""
echo "This will demonstrate:"
echo "  1. Running SecureScan against vulnerable code"
echo "  2. Showing detected vulnerabilities"
echo "  3. Displaying JSON output"
echo ""
echo "Recording in 3 seconds..."
sleep 3

clear

# Demo script
cat << 'DEMO_SCRIPT' > /tmp/securescan_demo.sh
#!/bin/bash
set -e

echo "======================================================================"
echo "  SecureScan Demo - Security Scanner Aggregator"
echo "======================================================================"
echo ""
echo "Step 1: Scan vulnerable application"
echo "----------------------------------------------------------------------"
echo ""
echo "$ python3 securescan.py --path test_project/"
echo ""
sleep 2

python3 securescan.py --path test_project/ --output demo_results.json

echo ""
echo "Step 2: View detailed JSON results"
echo "----------------------------------------------------------------------"
echo ""
sleep 2
echo "$ cat demo_results.json | jq '.findings[0]'"
cat demo_results.json | jq '.findings[0]'

echo ""
echo "Step 3: Summary statistics"
echo "----------------------------------------------------------------------"
echo ""
sleep 2
echo "$ cat demo_results.json | jq '{total: .summary.total_findings, by_severity: .summary.by_severity}'"
cat demo_results.json | jq '{total: .summary.total_findings, by_severity: .summary.by_severity}'

echo ""
echo "======================================================================"
echo "  Demo Complete!"
echo "======================================================================"
echo ""
echo "Key Features Demonstrated:"
echo "  ✓ Multi-tool aggregation (Semgrep, Bandit, Gitleaks)"
echo "  ✓ Deduplication algorithm"
echo "  ✓ Severity classification"
echo "  ✓ JSON output for CI/CD integration"
echo ""
DEMO_SCRIPT

chmod +x /tmp/securescan_demo.sh
cd /Users/deveshrana/PersonalProjectPortfolio/secengineeringprojects/securescan
bash /tmp/securescan_demo.sh

rm /tmp/securescan_demo.sh
