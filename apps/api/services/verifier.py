import json
import os
from urllib.parse import urlparse

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../../data/verified_platforms.json")

def load_verified_platforms():
    """Loads the whitelist JSON database."""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def extract_domain(url_or_domain: str) -> str:
    """Extracts clean root domain (e.g., 'https://www.apple.com/in/shop' -> 'apple.com')."""
    if not url_or_domain.startswith(("http://", "https://")):
        url_or_domain = "https://" + url_or_domain
    
    parsed = urlparse(url_or_domain)
    domain = parsed.netloc.lower()
    
    # Strip 'www.' if present
    if domain.startswith("www."):
        domain = domain[4:]
        
    return domain

def verify_url(url_or_domain: str):
    """
    Validates if a URL belongs to a genuine/verified platform.
    """
    clean_domain = extract_domain(url_or_domain)
    platforms = load_verified_platforms()

    for platform in platforms:
        # Check direct or subdomain match (e.g. apple.com or store.apple.com)
        if clean_domain == platform["domain"] or clean_domain.endswith("." + platform["domain"]):
            return {
                "input": url_or_domain,
                "domain": clean_domain,
                "is_verified": True,
                "trust_score": platform["trust_score"],
                "platform": platform
            }

    return {
        "input": url_or_domain,
        "domain": clean_domain,
        "is_verified": False,
        "trust_score": 0,
        "warning": "Unverified or high-risk domain. Exercise caution."
    }