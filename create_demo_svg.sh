#!/bin/bash
# Create SVG visualization of SecureScan demo output
# This creates a GitHub-friendly static image

cd /Users/deveshrana/PersonalProjectPortfolio/secengineeringprojects/securescan

# Run scan and capture output
python3 securescan.py --path test_project/ --output demo.json 2>&1 | tee scan_output.txt

# Create markdown with output for GitHub
cat > DEMO_OUTPUT.md << 'EOF'
# SecureScan Demo Output

## Running SecureScan

```bash
$ python3 securescan.py --path test_project/ --output demo.json
```

## Scan Output

```
EOF

cat scan_output.txt >> DEMO_OUTPUT.md

cat >> DEMO_OUTPUT.md << 'EOF'
```

## JSON Summary

```json
EOF

cat demo.json | python3 -c "import json, sys; data=json.load(sys.stdin); print(json.dumps(data['summary'], indent=2))" >> DEMO_OUTPUT.md

cat >> DEMO_OUTPUT.md << 'EOF'
```

## Sample Finding

```json
EOF

cat demo.json | python3 -c "import json, sys; data=json.load(sys.stdin); print(json.dumps(data['findings'][0], indent=2))" >> DEMO_OUTPUT.md

cat >> DEMO_OUTPUT.md << 'EOF'
```

## Key Features Demonstrated

- ✓ Multi-tool aggregation (Semgrep, Bandit, Gitleaks)
- ✓ Fingerprint-based deduplication
- ✓ 21 unique vulnerabilities detected
- ✓ Severity classification (HIGH/MEDIUM/LOW)
- ✓ JSON output for CI/CD integration

## GitHub Repository

🔗 [https://github.com/rana-devesh11/securescan](https://github.com/rana-devesh11/securescan)
EOF

echo "✓ Created DEMO_OUTPUT.md with full scan results"
rm scan_output.txt
