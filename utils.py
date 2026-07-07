from datetime import datetime
from pathlib import Path
import re

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()

def is_blank(value):
    return normalize_text(value) == "" or normalize_text(value).lower() in {"nan", "none"}

def looks_like_email(value):
    value = normalize_text(value).lower()
    if not value:
        return False
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))

def looks_like_url(value):
    value = normalize_text(value).lower()
    if not value:
        return False
    return value.startswith("http://") or value.startswith("https://")

def normalize_key(value):
    return re.sub(r"[^a-z0-9]+", "", normalize_text(value).lower())
