#!/bin/bash
# Automated SecureScan demo for asciinema recording
# This creates a professional demo with timing

# Configure terminal
export PS1="$ "
export TERM=xterm-256color

# Helper function for typing effect (looks more natural)
type_command() {
    echo -n "$ "
    for ((i=0; i<${#1}; i++)); do
        echo -n "${1:$i:1}"
        sleep 0.05
    done
    echo ""
    sleep 0.5
    eval "$1"
}

# Clear and start
clear
sleep 1

echo "======================================================================"
echo "  SecureScan - Security Scanner Aggregator Demo"
echo "======================================================================"
echo ""
echo "Multi-tool SAST + Secret Detection with Deduplication"
echo ""
sleep 2

echo "Step 1: Scanning vulnerable application..."
echo "----------------------------------------------------------------------"
sleep 1
type_command "python3 securescan.py --path test_project/ --output demo.json"

sleep 2
echo ""
echo "Step 2: Viewing detected vulnerabilities..."
echo "----------------------------------------------------------------------"
sleep 1
type_command "cat demo.json | python3 -m json.tool | head -50"

sleep 2
echo ""
echo "Step 3: Summary statistics..."
echo "----------------------------------------------------------------------"
sleep 1
type_command "cat demo.json | python3 -c \"import json, sys; data=json.load(sys.stdin); print(json.dumps(data['summary'], indent=2))\""

sleep 2
echo ""
echo "======================================================================"
echo "  Demo Complete!"
echo "======================================================================"
echo ""
echo "✓ Detected 21 unique security vulnerabilities"
echo "✓ SQL injection, command injection, weak crypto, hardcoded secrets"
echo "✓ Aggregated from Semgrep, Bandit, and Gitleaks"
echo "✓ Fingerprint-based deduplication"
echo ""
echo "GitHub: https://github.com/rana-devesh11/securescan"
echo ""
sleep 3
