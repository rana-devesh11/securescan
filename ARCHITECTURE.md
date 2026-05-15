# Architecture Documentation

## System Overview

SecureScan is a security scanner aggregator that normalizes and deduplicates findings from multiple tools. Built in Python for rapid development and ease of integration with security tools.

### Design Goals

- Tool-agnostic architecture using adapter pattern
- Minimal dependencies
- Fast execution (< 60 seconds for typical projects)
- Simple deployment (single Python script)

## Architecture Diagram

```
┌─────────────┐
│     CLI     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  SecurityScanner        │
│  - Orchestration        │
│  - State management     │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Tool Adapters          │
│  - run_semgrep()        │
│  - run_bandit()         │
│  - run_gitleaks()       │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Normalization          │
│  - parse_semgrep()      │
│  - parse_bandit()       │
│  - parse_gitleaks()     │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Deduplication Engine   │
│  - Fingerprinting       │
│  - Hash comparison      │
│  - Finding merger       │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Output Generator       │
│  - Console formatter    │
│  - JSON serializer      │
└─────────────────────────┘
```

## Component Details

### SecurityScanner Class

Central orchestrator managing scan lifecycle.

**Responsibilities:**
- Tool execution coordination
- Result aggregation
- Statistics generation

**Key Methods:**
```python
scan()                    # Main execution flow
run_<tool>()             # Tool-specific execution
parse_<tool>()           # Output normalization
deduplicate_findings()   # Deduplication logic
generate_summary()       # Statistics calculation
```

**Data Structure:**
```python
results = {
    "scan_id": str,           # Unique identifier
    "timestamp": str,         # ISO 8601 format
    "target": str,            # Scan path
    "tools": list,            # Tool metadata
    "findings": list,         # Deduplicated vulnerabilities
    "summary": dict           # Aggregated statistics
}
```

### Tool Adapters

Each adapter implements two methods:
1. `run_<tool>()` - Execute tool via subprocess
2. `parse_<tool>()` - Normalize output to common format

**Adapter Pattern Benefits:**
- Easy to add new tools
- Isolated tool-specific logic
- Consistent interface

**Common Finding Format:**
```python
{
    "tool": str,              # Tool name
    "rule_id": str,           # Tool-specific rule ID
    "severity": str,          # CRITICAL|HIGH|MEDIUM|LOW|INFO
    "file": str,              # File path
    "line": int,              # Line number
    "message": str,           # Finding description
    "category": str           # SAST|SCA|SECRETS|IAC
}
```

### Deduplication Engine

Uses cryptographic hashing for deterministic deduplication.

**Algorithm:**

```
1. Generate Fingerprint
   fingerprint = SHA256(file_path + ":" + line_number + ":" + severity)

2. Check Existence
   if fingerprint in seen_fingerprints:
       merge with existing finding
       add tool to detected_by array
   else:
       add as new finding

3. Calculate Metrics
   deduplication_rate = (duplicates / total) * 100
```

**Rationale for Fingerprint Components:**

- `file_path`: Identifies where vulnerability exists
- `line_number`: Pinpoints exact location
- `severity`: Groups by impact level

**Excluded from fingerprint:**
- `tool`: Different tools should match
- `message`: Phrasing varies across tools
- `rule_id`: Tool-specific identifiers

**Example:**

```python
# Semgrep finding
{
    "tool": "semgrep",
    "file": "app.py",
    "line": 22,
    "severity": "HIGH",
    "message": "Unsafe SQL query construction"
}

# Bandit finding
{
    "tool": "bandit",
    "file": "app.py",
    "line": 22,
    "severity": "HIGH",
    "message": "Possible SQL injection"
}

# Both generate same fingerprint
SHA256("app.py:22:HIGH") = "a3f2c8e1..."

# Merged result
{
    "file": "app.py",
    "line": 22,
    "severity": "HIGH",
    "detected_by": ["semgrep", "bandit"],
    "confidence": 85  # Increased due to multiple detections
}
```

## Data Flow

```
Input: /path/to/code
  |
  ▼
[Execute Tools]
  - semgrep  → 7 findings
  - bandit   → 15 findings
  - gitleaks → 1 finding
  |
  ▼
[Parse & Normalize]
  - Extract: file, line, severity, message
  - Map: tool-specific severity → standard severity
  - Format: tool output → common structure
  |
  ▼
[Fingerprint Generation]
  - For each finding: SHA256(file:line:severity)
  - Result: 23 fingerprints
  |
  ▼
[Deduplication]
  - Check fingerprint existence
  - Merge duplicates
  - Track detection sources
  |
  ▼
[Aggregation]
  - Count by severity
  - Count by category
  - Count by tool
  - Calculate deduplication rate
  |
  ▼
[Output]
  - Console: formatted display
  - JSON: machine-readable file
```

## Security Tool Integration

### Semgrep (SAST)

**Type:** Static analysis using semantic patterns  
**Method:** Pattern matching + AST analysis  
**Detection:** SQL injection, XSS, command injection, crypto issues

**Integration:**
```python
cmd = ["semgrep", "--config=auto", "--json", "--quiet", path]
result = subprocess.run(cmd, capture_output=True, text=True)
data = json.loads(result.stdout)
```

**Severity Mapping:**
```python
semgrep_to_standard = {
    "ERROR": "HIGH",
    "WARNING": "MEDIUM",
    "INFO": "LOW"
}
```

### Bandit (Python SAST)

**Type:** Python AST analyzer  
**Method:** Checks AST nodes against security patterns  
**Detection:** Hardcoded credentials, unsafe functions, weak crypto

**Integration:**
```python
cmd = ["bandit", "-r", path, "-f", "json", "-q"]
result = subprocess.run(cmd, capture_output=True, text=True)
data = json.loads(result.stdout)
```

**Why Both Semgrep and Bandit:**
- Different detection methods (pattern vs AST)
- Overlapping coverage increases confidence
- Deduplication handles redundancy

### Gitleaks (Secret Detection)

**Type:** Secret scanner  
**Method:** Regex patterns + entropy analysis  
**Detection:** API keys, tokens, credentials

**Integration:**
```python
cmd = ["gitleaks", "detect", "--source", path, 
       "--report-format", "json", "--report-path", report_file]
result = subprocess.run(cmd, capture_output=True, text=True)
```

**Detection Methods:**
- Regex: Matches known secret patterns (AWS keys, GitHub tokens)
- Entropy: Identifies high-entropy strings
- Context: Variable names like "password", "secret"

## Design Decisions

### Sequential vs Parallel Execution

**Current:** Sequential  
**Rationale:** Simpler implementation, easier debugging  
**Trade-off:** ~60 seconds total vs potential ~20 seconds parallel

### Simple vs Fuzzy Matching

**Current:** Exact fingerprint matching  
**Rationale:** Fast (O(1) lookup), deterministic  
**Trade-off:** Misses near-duplicates (e.g., line 22 vs 24)

### In-Memory vs Database

**Current:** In-memory Python dictionaries  
**Rationale:** No external dependencies, fast for single scans  
**Trade-off:** No historical tracking, no trend analysis

### JSON vs SARIF

**Current:** Custom JSON format  
**Rationale:** Simple, easy to parse  
**Trade-off:** Not compatible with GitHub Code Scanning

## Performance Characteristics

**Benchmark Environment:**
- Project: 1000 files, 50k LOC
- Hardware: MacBook Pro M1
- Tools: Semgrep, Bandit, Gitleaks

**Results:**

| Tool | Execution Time | Findings |
|------|---------------|----------|
| Semgrep | 25-35s | 45 |
| Bandit | 10-15s | 38 |
| Gitleaks | 5-10s | 12 |
| Total | 40-60s | 95 |
| Deduplication | 0.1s | 32 unique |
| **Reduction** | - | **66%** |

**Complexity:**
- Tool execution: O(n) where n = lines of code
- Deduplication: O(m) where m = number of findings
- Overall: O(n + m)

## Scalability Considerations

**Current Limitations:**
- Single-threaded execution
- No caching mechanism
- Full repository scan each time
- In-memory only (no persistence)

**Potential Improvements:**

1. **Parallel Execution**
   ```python
   with ThreadPoolExecutor() as executor:
       futures = [
           executor.submit(self.run_semgrep),
           executor.submit(self.run_bandit),
           executor.submit(self.run_gitleaks)
       ]
   ```

2. **Incremental Scanning**
   - Use git diff to scan only changed files
   - Cache results for unchanged files

3. **Distributed Execution**
   - Message queue (Redis/RabbitMQ)
   - Worker pool for parallel scans
   - Results aggregation service

4. **Database Layer**
   - PostgreSQL for findings storage
   - Track vulnerability lifecycle
   - Historical trend analysis

## Testing

**Current Tests:**
- Manual testing with test_project/vulnerable_app.py
- Validates 23 known vulnerabilities detected

**Test Coverage:**
- Tool execution: Manual verification
- Output parsing: Manual verification
- Deduplication: Manual verification

## Security Considerations

**Tool Isolation:**
- Each tool runs in subprocess
- No shared state between tools
- Timeouts prevent hanging

**Input Validation:**
- Path validation before scanning
- Tool availability checks
- Output format validation

**Secrets Handling:**
- Test secrets clearly marked as fake
- Real secrets never committed
- Detection demonstrates capability without exposure

## References

### Security Standards
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SARIF Specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)

### Tools
- [Semgrep Documentation](https://semgrep.dev/docs/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)

### Related Work
- [Dependabot](https://github.com/dependabot) - Dependency vulnerability scanning
- [CodeQL](https://codeql.github.com/) - Semantic code analysis
- [DefectDojo](https://www.defectdojo.org/) - Security findings management

---

**Author:** Devesh Rana  
**Last Updated:** May 2026
