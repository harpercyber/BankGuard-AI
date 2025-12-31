from faker import Faker
import datetime
import uuid
from random import random
from random import choice, random, randint

# Define home regions with corresponding IP prefixes
REGION_IP_RANGES = {
    "US_EAST": ["10.10.", "10.11."],
    "US_WEST": ["10.20.", "10.21."],
    "EU_CENTRAL": ["10.30.", "10.31."],
    "ASIA_EAST": ["10.40.", "10.41."],
}


def label_event(event:dict) -> dict:
    """
    Accepts a single log (dictionary) and labels it as normal or suspicious based on your defined rules.
    """
    #Creates a list that will append reasons for a user being suspicious based on conditions they trigger
    reasons = []

    #adds failed logins as a reason
    if not event.get("login_success", True):
        reasons.append("failed login")

    #if transaction amount higher than $5000 then it is added as a suspicious reason
    if event.get("transaction amount", 0) > 5000:
        reasons.append("high transaction")

    # Rule 3: home region vs IP region mismatch
    ip_region = get_ip_region(event.get("IP_address", ""))

    if ip_region and ip_region != event.get("home_region"):
        reasons.append("ip region mismatch")

        
    event["is_suspicious"] = len(reasons) > 0
    #gives each log a explanation for why its suspicious or marks it as normal if not
    event["reason"] = ",".join(reasons) if reasons else "normal"
    event["risk_level"] = len(reasons)

    return event

def get_ip_region(ip_address: str) -> str | None:
    """
    Determines which region an IP belongs to based on prefix matching.
    Returns the region name or None if no match is found.
    """
    for region, prefixes in REGION_IP_RANGES.items():
        for prefix in prefixes:
            if ip_address.startswith(prefix):
                return region
    return None

