#!/usr/bin/env python3
"""
SecureScan - Security Tool Aggregator
Author: Devesh Rana (OSCP+, AWS Security Specialty)
A simple CLI tool that runs multiple security scanners and aggregates results
"""

import subprocess
import json
import sys
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class SecurityScanner:
    """Main scanner orchestrator"""

    def __init__(self, target_path="."):
        self.target_path = Path(target_path)
        self.results = {
            "scan_id": self.generate_scan_id(),
            "timestamp": datetime.now().isoformat(),
            "target": str(self.target_path),
            "tools": [],
            "findings": [],
            "summary": {}
        }

    def generate_scan_id(self):
        """Generate unique scan ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(timestamp.encode()).hexdigest()[:8]

    def run_semgrep(self):
        """Run Semgrep SAST scanner"""
        print("[*] Running Semgrep...")
        try:
            cmd = [
                "semgrep",
                "--config=auto",
                "--json",
                "--quiet",
                str(self.target_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode in [0, 1]:  # 0 = no findings, 1 = findings found
                data = json.loads(result.stdout)
                findings = self.parse_semgrep(data)
                self.results["tools"].append({"name": "semgrep", "findings": len(findings)})
                return findings
            else:
                print(f"[!] Semgrep failed: {result.stderr}")
                return []
        except FileNotFoundError:
            print("[!] Semgrep not installed. Install: brew install semgrep")
            return []
        except Exception as e:
            print(f"[!] Semgrep error: {e}")
            return []

    def parse_semgrep(self, data):
        """Parse Semgrep JSON output"""
        findings = []
        for result in data.get("results", []):
            finding = {
                "tool": "semgrep",
                "rule_id": result.get("check_id", "unknown"),
                "severity": result.get("extra", {}).get("severity", "INFO").upper(),
                "file": result.get("path", ""),
                "line": result.get("start", {}).get("line", 0),
                "message": result.get("extra", {}).get("message", ""),
                "category": "SAST"
            }
            findings.append(finding)
        return findings

    def run_bandit(self):
        """Run Bandit Python security scanner"""
        print("[*] Running Bandit...")
        try:
            cmd = [
                "bandit",
                "-r", str(self.target_path),
                "-f", "json",
                "-q"  # Quiet mode
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode in [0, 1]:
                data = json.loads(result.stdout)
                findings = self.parse_bandit(data)
                self.results["tools"].append({"name": "bandit", "findings": len(findings)})
                return findings
            else:
                return []
        except FileNotFoundError:
            print("[!]  Bandit not installed. Install: pip install bandit")
            return []
        except Exception as e:
            print(f"[!]  Bandit error: {e}")
            return []

    def parse_bandit(self, data):
        """Parse Bandit JSON output"""
        findings = []
        for result in data.get("results", []):
            severity_map = {"HIGH": "HIGH", "MEDIUM": "MEDIUM", "LOW": "LOW"}
            finding = {
                "tool": "bandit",
                "rule_id": result.get("test_id", "unknown"),
                "severity": severity_map.get(result.get("issue_severity", "LOW"), "LOW"),
                "file": result.get("filename", ""),
                "line": result.get("line_number", 0),
                "message": result.get("issue_text", ""),
                "category": "SAST"
            }
            findings.append(finding)
        return findings

    def run_gitleaks(self):
        """Run Gitleaks secret scanner"""
        print("[*] Running Gitleaks...")
        try:
            cmd = [
                "gitleaks",
                "detect",
                "--source", str(self.target_path),
                "--report-format", "json",
                "--report-path", "/tmp/gitleaks-report.json",
                "--no-git"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            # Gitleaks returns 1 if leaks found, 0 if none
            report_path = Path("/tmp/gitleaks-report.json")
            if report_path.exists():
                with open(report_path) as f:
                    data = json.load(f)
                    findings = self.parse_gitleaks(data)
                    self.results["tools"].append({"name": "gitleaks", "findings": len(findings)})
                    report_path.unlink()  # Clean up
                    return findings
            return []
        except FileNotFoundError:
            print("[!]  Gitleaks not installed. Install: brew install gitleaks")
            return []
        except Exception as e:
            print(f"[!]  Gitleaks error: {e}")
            return []

    def parse_gitleaks(self, data):
        """Parse Gitleaks JSON output"""
        findings = []
        if not data:
            return findings

        for result in data:
            finding = {
                "tool": "gitleaks",
                "rule_id": result.get("RuleID", "secret-detected"),
                "severity": "HIGH",  # Secrets are always high severity
                "file": result.get("File", ""),
                "line": result.get("StartLine", 0),
                "message": f"Secret detected: {result.get('Description', 'Unknown secret type')}",
                "category": "SECRETS"
            }
            findings.append(finding)
        return findings

    def deduplicate_findings(self, all_findings):
        """Remove duplicate findings using fingerprinting"""
        print("[>] Deduplicating findings...")

        unique_findings = {}
        duplicate_count = 0

        for finding in all_findings:
            # Create fingerprint: file + line + severity
            fingerprint = f"{finding['file']}:{finding['line']}:{finding['severity']}"

            if fingerprint in unique_findings:
                # Duplicate found - merge tool names
                existing = unique_findings[fingerprint]
                if finding['tool'] not in existing.get('detected_by', []):
                    if 'detected_by' not in existing:
                        existing['detected_by'] = [existing['tool']]
                    existing['detected_by'].append(finding['tool'])
                duplicate_count += 1
            else:
                finding['detected_by'] = [finding['tool']]
                unique_findings[fingerprint] = finding

        deduplication_rate = (duplicate_count / len(all_findings) * 100) if all_findings else 0

        return list(unique_findings.values()), duplicate_count, deduplication_rate

    def generate_summary(self, findings):
        """Generate scan summary statistics"""
        summary = {
            "total_findings": len(findings),
            "by_severity": defaultdict(int),
            "by_category": defaultdict(int),
            "by_tool": defaultdict(int)
        }

        for finding in findings:
            summary["by_severity"][finding["severity"]] += 1
            summary["by_category"][finding["category"]] += 1
            for tool in finding.get("detected_by", [finding["tool"]]):
                summary["by_tool"][tool] += 1

        return dict(summary)

    def scan(self):
        """Run all scanners and aggregate results"""
        print("\n" + "="*60)
        print("[#]  SecureScan - Security Tool Aggregator")
        print("="*60)
        print(f"Target: Target: {self.target_path}")
        print(f"Scan ID: Scan ID: {self.results['scan_id']}")
        print(f"Started: Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")

        # Run all available scanners
        all_findings = []
        all_findings.extend(self.run_semgrep())
        all_findings.extend(self.run_bandit())
        all_findings.extend(self.run_gitleaks())

        print(f"\n[*] Raw findings: {len(all_findings)}")

        # Deduplicate
        unique_findings, duplicates, dedup_rate = self.deduplicate_findings(all_findings)

        print(f"[+] Unique findings: {len(unique_findings)}")
        print(f"[>] Duplicates removed: {duplicates} ({dedup_rate:.1f}%)")

        # Store results
        self.results["findings"] = unique_findings
        self.results["summary"] = self.generate_summary(unique_findings)
        self.results["summary"]["duplicates_removed"] = duplicates
        self.results["summary"]["deduplication_rate"] = f"{dedup_rate:.1f}%"

        return self.results

    def print_results(self):
        """Print results to console"""
        print("\n" + "="*60)
        print("[=] SCAN RESULTS")
        print("="*60 + "\n")

        summary = self.results["summary"]

        # Print summary
        print(f"Total Findings: {summary['total_findings']}")
        print(f"Duplicates Removed: {summary['duplicates_removed']} ({summary['deduplication_rate']})\n")

        # By severity
        print("By Severity:")
        severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
        severity_icons = {"CRITICAL": "🔴", "HIGH": "[HIGH]", "MEDIUM": "[MED]", "LOW": "[LOW]", "INFO": "🔵"}
        for severity in severity_order:
            count = summary["by_severity"].get(severity, 0)
            if count > 0:
                icon = severity_icons.get(severity, "[!]")
                print(f"  {icon} {severity:8} : {count}")

        print("\nBy Category:")
        for category, count in summary["by_category"].items():
            print(f"  - {category:10} : {count}")

        print("\nBy Tool:")
        for tool, count in summary["by_tool"].items():
            print(f"  - {tool:10} : {count}")

        # Print top findings
        if self.results["findings"]:
            print("\n" + "="*60)
            print("[*] TOP FINDINGS (First 10)")
            print("="*60 + "\n")

            for idx, finding in enumerate(self.results["findings"][:10], 1):
                severity = finding["severity"]
                icon = severity_icons.get(severity, "[!]")
                tools = ", ".join(finding.get("detected_by", [finding["tool"]]))

                print(f"{idx}. {icon} {severity} - {finding['file']}:{finding['line']}")
                print(f"   Tools: {tools}")
                print(f"   {finding['message']}")
                print()

        print("="*60)

    def save_results(self, output_file="scan_results.json"):
        """Save results to JSON file"""
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n[+] Results saved to: {output_path.absolute()}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="SecureScan - Security Tool Aggregator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan current directory
  python securescan.py

  # Scan specific path
  python securescan.py --path /path/to/code

  # Save results to file
  python securescan.py --output results.json
        """
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Path to scan (default: current directory)"
    )
    parser.add_argument(
        "--output",
        default="scan_results.json",
        help="Output file for results (default: scan_results.json)"
    )

    args = parser.parse_args()

    # Run scan
    scanner = SecurityScanner(args.path)
    scanner.scan()
    scanner.print_results()
    scanner.save_results(args.output)


if __name__ == "__main__":
    main()
