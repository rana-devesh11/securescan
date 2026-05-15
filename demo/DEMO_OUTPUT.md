# SecureScan Demo Output

## Running SecureScan

```bash
$ python3 securescan.py --path test_project/ --output demo.json
```

## Scan Output

```

============================================================
🛡️  SecureScan - Security Tool Aggregator
============================================================
📁 Target: test_project
🆔 Scan ID: 3c8855f5
⏰ Started: 2026-05-10 17:43:04
============================================================

🔍 Running Semgrep...
🔍 Running Bandit...
🔍 Running Gitleaks...

📊 Raw findings: 21
🔄 Deduplicating findings...
✨ Unique findings: 21
🔄 Duplicates removed: 0 (0.0%)

============================================================
📋 SCAN RESULTS
============================================================

Total Findings: 21
Duplicates Removed: 0 (0.0%)

By Severity:
  🟠 HIGH     : 3
  🟡 MEDIUM   : 4
  🟢 LOW      : 8

By Category:
  • SAST       : 21

By Tool:
  • semgrep    : 6
  • bandit     : 15

============================================================
🔍 TOP FINDINGS (First 10)
============================================================

1. ⚪ WARNING - test_project/vulnerable_app.py:23
   Tools: semgrep
   Detected possible formatted SQL query. Use parameterized queries instead.

2. ⚪ ERROR - test_project/vulnerable_app.py:23
   Tools: semgrep
   Avoiding SQL string concatenation: untrusted input concatenated with raw SQL query can result in SQL Injection. In order to execute raw query safely, prepared statement should be used. SQLAlchemy provides TextualSQL to easily used prepared statement with named parameters. For complex SQL composition, use SQL Expression Language or Schema Definition Language. In most cases, SQLAlchemy ORM will be a better option.

3. ⚪ ERROR - test_project/vulnerable_app.py:33
   Tools: semgrep
   Found 'subprocess' function 'call' with 'shell=True'. This is dangerous because this call will spawn the command using a shell process. Doing so propagates current shell settings and variables, which makes it much easier for a malicious actor to execute commands. Use 'shell=False' instead.

4. ⚪ WARNING - test_project/vulnerable_app.py:47
   Tools: semgrep
   It looks like MD5 is used as a password hash. MD5 is not considered a secure password hash because it can be cracked by an attacker in a short amount of time. Use a suitable password hashing function such as scrypt. You can use `hashlib.scrypt`.

5. ⚪ WARNING - test_project/vulnerable_app.py:55
   Tools: semgrep
   Avoid using `pickle`, which is known to lead to code execution vulnerabilities. When unpickling, the serialized data could be manipulated to run arbitrary code. Instead, consider serializing the relevant data as JSON or a similar text-based serialization format.

6. ⚪ WARNING - test_project/vulnerable_app.py:72
   Tools: semgrep
   Detected the use of eval(). eval() can be dangerous if used to evaluate dynamic content. If this content can be input from outside the program, this may be a code injection vulnerability. Ensure evaluated content is not definable by external sources.

7. 🟢 LOW - test_project/vulnerable_app.py:8
   Tools: bandit
   Consider possible security implications associated with the subprocess module.

8. 🟢 LOW - test_project/vulnerable_app.py:13
   Tools: bandit
   Possible hardcoded password: 'FAKE_aws_secret_FOR_TESTING_PURPOSES_ONLY'

9. 🟢 LOW - test_project/vulnerable_app.py:14
   Tools: bandit
   Possible hardcoded password: 'test_password_123_NOT_REAL'

10. 🟡 MEDIUM - test_project/vulnerable_app.py:22
   Tools: bandit
   Possible SQL injection vector through string-based query construction.

============================================================

💾 Results saved to: /Users/deveshrana/PersonalProjectPortfolio/secengineeringprojects/securescan/demo.json
```

## JSON Summary

```json
{
  "total_findings": 21,
  "by_severity": {
    "WARNING": 4,
    "ERROR": 2,
    "LOW": 8,
    "MEDIUM": 4,
    "HIGH": 3
  },
  "by_category": {
    "SAST": 21
  },
  "by_tool": {
    "semgrep": 6,
    "bandit": 15
  },
  "duplicates_removed": 0,
  "deduplication_rate": "0.0%"
}
```

## Sample Finding

```json
{
  "tool": "semgrep",
  "rule_id": "python.lang.security.audit.formatted-sql-query.formatted-sql-query",
  "severity": "WARNING",
  "file": "test_project/vulnerable_app.py",
  "line": 23,
  "message": "Detected possible formatted SQL query. Use parameterized queries instead.",
  "category": "SAST",
  "detected_by": [
    "semgrep"
  ]
}
```

## Key Features Demonstrated

- ✓ Multi-tool aggregation (Semgrep, Bandit, Gitleaks)
- ✓ Fingerprint-based deduplication
- ✓ 21 unique vulnerabilities detected
- ✓ Severity classification (HIGH/MEDIUM/LOW)
- ✓ JSON output for CI/CD integration

## GitHub Repository

🔗 [https://github.com/rana-devesh11/securescan](https://github.com/rana-devesh11/securescan)
