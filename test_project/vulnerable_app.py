"""
Test application with intentional security vulnerabilities
For testing SecureScan
"""

import os
import sqlite3
import subprocess

# Hardcoded secrets (FAKE TEST DATA - will be detected by Gitleaks)
# These are intentionally vulnerable examples for testing purposes only
API_KEY = "sk_test_FAKE_KEY_FOR_TESTING_ONLY_1234567890"
AWS_SECRET = "FAKE_aws_secret_FOR_TESTING_PURPOSES_ONLY"
DATABASE_PASSWORD = "test_password_123_NOT_REAL"

def sql_injection_vulnerable(user_id):
    """SQL Injection vulnerability"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Unsafe SQL query (will be detected by Bandit and Semgrep)
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

    return cursor.fetchone()

def command_injection_vulnerable(filename):
    """Command Injection vulnerability"""
    # Unsafe command execution (will be detected by Bandit and Semgrep)
    os.system(f"cat {filename}")

    # Another variant
    subprocess.call(f"ls -la {filename}", shell=True)

def path_traversal_vulnerable(user_file):
    """Path Traversal vulnerability"""
    # No path validation (will be detected by Semgrep)
    file_path = f"/var/data/{user_file}"
    with open(file_path, 'r') as f:
        return f.read()

def weak_crypto():
    """Weak cryptography"""
    import hashlib

    # MD5 is weak (will be detected by Bandit)
    password_hash = hashlib.md5(b"password123").hexdigest()
    return password_hash

def insecure_deserialization(data):
    """Insecure deserialization"""
    import pickle

    # Unsafe pickle (will be detected by Bandit)
    user_data = pickle.loads(data)
    return user_data

class InsecureConfig:
    """Insecure configuration"""

    def __init__(self):
        # Hardcoded credentials
        self.db_host = "localhost"
        self.db_user = "admin"
        self.db_password = "admin123"  # Weak password
        self.debug = True
        self.secret_key = "hardcoded_secret_key_12345"

def eval_vulnerability(user_input):
    """Code injection via eval"""
    # Dangerous eval (will be detected by Bandit and Semgrep)
    result = eval(user_input)
    return result

def xxe_vulnerable(xml_data):
    """XML External Entity (XXE) vulnerability"""
    import xml.etree.ElementTree as ET

    # Unsafe XML parsing (will be detected)
    root = ET.fromstring(xml_data)
    return root

# More hardcoded secrets (FAKE TEST DATA ONLY)
STRIPE_KEY = "FAKE_test_key_FOR_DEMO_PURPOSES_ONLY"
JWT_SECRET = "FAKE_jwt_secret_NOT_REAL_FOR_TESTING"

if __name__ == "__main__":
    print("This is a vulnerable application for testing")
    print(f"API Key: {API_KEY[:10]}...")
