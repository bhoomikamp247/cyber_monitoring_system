import re

def has_ip_address(url: str) -> bool:
    return bool(re.search(r"http[s]?://(\d{1,3}\.){3}\d{1,3}", url))

def is_suspicious_domain(url: str) -> bool:
    suspicious_patterns = ["free", "bonus", "verify", "login", "security-check",
                           "update-account", "limited-offer"]
    return any(pattern in url.lower() for pattern in suspicious_patterns)

def contains_malicious_keywords(url: str) -> bool:
    keywords = ["bank", "paypal", "password", "credit", "otp", "confirm"]
    return any(k in url.lower() for k in keywords)

def analyze_url(url: str):
    result = {"url": url, "safe": True, "warnings": []}

    if has_ip_address(url):
        result["safe"] = False
        result["warnings"].append("URL contains IP address instead of domain.")

    if is_suspicious_domain(url):
        result["safe"] = False
        result["warnings"].append("Domain name looks suspicious or fake.")

    if contains_malicious_keywords(url):
        result["safe"] = False
        result["warnings"].append("URL contains phishing-related keywords.")

    result["summary"] = "No major threats detected." if result["safe"] else "Potential risk detected. Use caution."
    return result


