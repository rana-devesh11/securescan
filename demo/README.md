# SecureScan Demo

Creating terminal outputs and recordings to showcase SecureScan for portfolio/LinkedIn.

## Quick Demo (2 minutes)

```bash
# Run scan
python3 securescan.py --path test_project/ --output demo.json

# Show results
cat demo.json | python3 -m json.tool | less
```

## Recording Terminal Demo

### Option 1: asciinema (Recommended - GitHub embeddable)

```bash
# Install
brew install asciinema

# Record demo
asciinema rec securescan-demo.cast
python3 securescan.py --path test_project/
cat demo.json | python3 -m json.tool | head -50
# Press Ctrl+D to stop

# Upload to asciinema.org
asciinema upload securescan-demo.cast

# Embed in README with returned URL
```

### Option 2: Animated GIF

```bash
# Install terminalizer
npm install -g terminalizer

# Record
terminalizer record securescan-demo

# Inside recording:
python3 securescan.py --path test_project/
cat demo.json | python3 -c "import json, sys; print(json.dumps(json.load(sys.stdin)['summary'], indent=2))"
# Press Ctrl+D

# Render to GIF
terminalizer render securescan-demo

# Result: securescan-demo.gif (add to README)
```

### Option 3: Screen Recording (macOS)

```bash
# Press Cmd+Shift+5
# Select "Record Selected Portion"
# Click terminal window
# Click "Record"
# Run: python3 securescan.py --path test_project/
# Stop from menu bar
# Save as securescan-demo.mov
```

## Terminal outputs to Capture

### 1. Scan Running
```bash
python3 securescan.py --path test_project/
```
Capture: Terminal showing colored output, progress indicators

### 2. Results Summary
```bash
cat demo.json | python3 -c "import json, sys; d=json.load(sys.stdin); print(json.dumps(d['summary'], indent=2))"
```
Capture: Summary statistics with severity breakdown

### 3. Individual Finding
```bash
cat demo.json | python3 -c "import json, sys; d=json.load(sys.stdin); print(json.dumps(d['findings'][0], indent=2))"
```
Capture: Detailed finding with file, line, severity

### 4. Deduplication Stats
Highlight in scan output:
```
📊 Raw findings: 21
🔄 Deduplicating findings...
✨ Unique findings: 21
🔄 Duplicates removed: 0 (0.0%)
```

## LinkedIn Post Template

```
🛡️ SecureScan: Security Scanner Aggregator

Built a tool that combines Semgrep, Bandit, and Gitleaks into a unified security scanning pipeline.

Key Features:
✅ Fingerprint-based deduplication using SHA256
✅ Aggregates SAST + secret detection
✅ Severity classification (HIGH/MEDIUM/LOW)
✅ JSON output for CI/CD integration

Detected 21 vulnerabilities including:
• SQL injection (Semgrep)
• Command injection (Semgrep)
• Hardcoded secrets (Bandit)
• Weak crypto (Semgrep)

Tech: Python, adapter pattern, security tooling integration

[Attach: Terminal output or GIF]

🔗 GitHub: github.com/rana-devesh11/securescan

#CyberSecurity #AppSec #SAST #Python #SecurityEngineering
```

## Video Script (1-2 minutes)

```
[0:00] "Hi, I'm Devesh. I built SecureScan, a security scanner aggregator."

[0:05] "It combines three tools - Semgrep for SAST, Bandit for Python security, and Gitleaks for secret detection."

[0:10] [Show terminal] "Let me show you how it works."

[0:12] "I'll scan this vulnerable application."
[Run: python3 securescan.py --path test_project/]

[0:15] [Point to output] "SecureScan runs all three tools in parallel."

[0:20] [Point to deduplication] "The key feature is deduplication - it uses SHA256 fingerprints to identify duplicate findings across tools."

[0:30] [Show results] "It found 21 unique vulnerabilities - SQL injection, command injection, weak crypto, and hardcoded secrets."

[0:40] [Show JSON] "The output is JSON, making it easy to integrate into CI/CD pipelines."

[0:45] "This demonstrates security tool integration, adapter pattern, and practical AppSec engineering."

[0:50] "Check out the code on GitHub - link in description."
```

## Tools Installation

```bash
# asciinema (terminal recording)
brew install asciinema

# terminalizer (animated GIF)
npm install -g terminalizer

# jq (JSON formatting)
brew install jq

# Python dependencies
pip install -r requirements.txt
```

## Tips

1. **Clean Terminal**: Use `clear` before recording
2. **Readable Font**: Set terminal font to 14-16pt
3. **Color Scheme**: Use professional theme (Solarized, Dracula)
4. **Timing**: Add 2-second pauses between commands
5. **Keep Short**: 2-3 minutes max for videos
6. **Show Real Results**: No fake data - actual tool output
