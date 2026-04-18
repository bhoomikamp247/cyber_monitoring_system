import re

# Rule: Detect if URL has an IP address
def has_ip_address(url: str) -> bool:
    return bool(re.search(r"http[s]?://(\d{1,3}\.){3}\d{1,3}", url))

# Rule: Detect suspicious/fake domains
def is_suspicious_domain(url: str) -> bool:
    suspicious_patterns = [
        "free", "bonus", "verify", "login", "security-check",
        "update-account", "limited-offer"
    ]
    return any(pattern in url.lower() for pattern in suspicious_patterns)

# Rule: Detect malware/phishing keywords
def contains_malicious_keywords(url: str) -> bool:
    keywords = ["bank", "paypal", "password", "credit", "otp", "confirm"]
    return any(k in url.lower() for k in keywords)

