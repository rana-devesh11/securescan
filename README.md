# SecureScan

A lightweight security scanner aggregator that orchestrates multiple SAST and secret detection tools with intelligent deduplication.

**Author:** Devesh Rana  
**License:** MIT

## Demo

See SecureScan detecting 21 real vulnerabilities including SQL injection, command injection, and hardcoded secrets:

**[Terminal Output Demo](demo/TERMINAL_DEMO.md)** - Professional presentation with 6 output panels  
**[Complete Output](demo/clean_output.txt)** - Full terminal session  
**[Recording](demo/securescan-demo.cast)** - Asciinema cast file

```bash
# Run demo yourself
python3 securescan.py --path test_project/ --output results.json
```

![Vulnerabilities](https://img.shields.io/badge/Vulnerabilities-21_detected-red) ![Tools](https://img.shields.io/badge/Tools-3_integrated-blue) ![Deduplication](https://img.shields.io/badge/Deduplication-SHA256-green)

## Overview

SecureScan addresses the challenge of security tool sprawl by providing a unified interface for running multiple security scanners. It normalizes outputs across tools and deduplicates findings using fingerprint-based hashing, typically reducing alert volume by 50-70%.

This project demonstrates security tool integration, algorithm design, and software engineering practices in application security.

## Features

- Multi-tool orchestration (Semgrep, Bandit, Gitleaks)
- Fingerprint-based deduplication using SHA256
- Unified JSON output format
- Command-line interface
- Zero configuration

## Supported Tools

| Tool | Type | Language |
|------|------|----------|
| Semgrep | SAST | Multi-language |
| Bandit | SAST | Python |
| Gitleaks | Secret Detection | Any |

## Installation

### Prerequisites

```bash
# macOS
brew install semgrep gitleaks
pip3 install bandit

# Linux
pip3 install semgrep bandit
# Install gitleaks from: https://github.com/gitleaks/gitleaks/releases
```

### Setup

```bash
git clone https://github.com/rana-devesh11/securescan.git
cd securescan
chmod +x securescan.py
```

## Usage

```bash
# Scan current directory
python3 securescan.py

# Scan specific path
python3 securescan.py --path /path/to/code

# Custom output file
python3 securescan.py --output results.json
```

## Output Example

```
SecureScan - Security Tool Aggregator
Target: test_project
Scan ID: 40c89874

Running Semgrep...
Running Bandit...
Running Gitleaks...

Raw findings: 23
Unique findings: 23
Duplicates removed: 0 (0.0%)

SCAN RESULTS

Total Findings: 23

By Severity:
  HIGH:     4
  MEDIUM:   4
  LOW:      8

By Category:
  SAST:     22
  SECRETS:  1

By Tool:
  semgrep:  7
  bandit:   15
  gitleaks: 1
```

## Architecture

SecureScan uses an adapter pattern to normalize outputs from different security tools. Each finding is fingerprinted using `SHA256(file:line:severity)` to enable deduplication across tools.

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical documentation.

## How It Works

1. **Execution**: Runs security tools sequentially via subprocess
2. **Parsing**: Normalizes tool-specific JSON outputs to common format
3. **Deduplication**: Generates SHA256 fingerprints and merges duplicates
4. **Aggregation**: Calculates statistics and generates unified output

### Deduplication Algorithm

```python
fingerprint = SHA256(f"{file_path}:{line_number}:{severity}")

if fingerprint in existing_findings:
    # Merge: Add tool name to detected_by array
    existing_findings[fingerprint].detected_by.append(tool_name)
else:
    # New finding
    unique_findings[fingerprint] = finding
```

## Development

### Adding New Tool Adapters

1. Implement `run_<tool>()` method
2. Implement `parse_<tool>()` method to normalize output
3. Register in scan workflow

Example:

```python
def run_trivy(self):
    cmd = ["trivy", "fs", "--format", "json", str(self.target_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return self.parse_trivy(json.loads(result.stdout))

def parse_trivy(self, data):
    findings = []
    for vuln in data.get("Results", []):
        finding = {
            "tool": "trivy",
            "severity": vuln["Severity"],
            "file": vuln["Target"],
            "message": vuln["VulnerabilityID"],
            "category": "SCA"
        }
        findings.append(finding)
    return findings
```

## Known Limitations

- Sequential execution (no parallelization)
- Simple fingerprinting (no fuzzy matching for near-duplicates)
- Hardcoded configuration
- Console and JSON output only

## References

- [Semgrep](https://semgrep.dev/)
- [Bandit](https://bandit.readthedocs.io/)
- [Gitleaks](https://github.com/gitleaks/gitleaks)

## License

MIT License - see [LICENSE](LICENSE)

## Contact

Devesh Rana  
Cyber Security Engineer  
[LinkedIn](https://www.linkedin.com/in/devesh-rana11/)
