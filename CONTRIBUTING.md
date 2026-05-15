# Contributing

This project is primarily a demonstration of security engineering concepts. Contributions are welcome if you find it useful.

## Development Setup

```bash
git clone https://github.com/rana-devesh11/securescan.git
cd securescan
pip3 install -r requirements.txt
brew install semgrep gitleaks
```

## Adding Tool Adapters

1. Implement `run_<tool>()` method in SecurityScanner class
2. Implement `parse_<tool>()` method to normalize output
3. Register tool in `scan()` method
4. Update README.md with tool information

Example structure:

```python
def run_mytool(self):
    """Run MyTool scanner"""
    try:
        cmd = ["mytool", "scan", "--json", str(self.target_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode in [0, 1]:
            data = json.loads(result.stdout)
            findings = self.parse_mytool(data)
            self.results["tools"].append({"name": "mytool", "findings": len(findings)})
            return findings
        return []
    except Exception as e:
        print(f"MyTool error: {e}")
        return []

def parse_mytool(self, data):
    """Parse MyTool JSON output"""
    findings = []
    for item in data.get("results", []):
        finding = {
            "tool": "mytool",
            "rule_id": item.get("id"),
            "severity": self.map_severity(item.get("severity")),
            "file": item.get("file"),
            "line": item.get("line"),
            "message": item.get("message"),
            "category": "SAST"  # or SCA, SECRETS, IAC
        }
        findings.append(finding)
    return findings
```

## Code Style

- Follow PEP 8
- Use docstrings for methods
- Keep methods focused
- Handle errors gracefully

## Testing

Test your changes:

```bash
python3 securescan.py --path test_project
```

Expected output: 23 findings detected

## Pull Requests

- Create feature branch from main
- Keep changes focused
- Update documentation if needed
- Test before submitting

## Questions

Open an issue for questions or suggestions.
