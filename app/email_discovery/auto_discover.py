from pathlib import Path
import sys
import re
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.email_discovery.config import BATCH_FOLDER, RESULTS_FOLDER
from app.email_discovery.validation import is_valid_email


EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
COMMON_PATHS = ["", "/contact", "/contact-us", "/about", "/about-us"]


def find_current_email_batch():
    batches = sorted(BATCH_FOLDER.glob("email_batch_*.csv"))
    for batch in batches:
        result_file = RESULTS_FOLDER / batch.name.replace(".csv", "_interactive_results.csv")
        if not result_file.exists():
            return batch
    return batches[0] if batches else None


def fetch(url):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "203local Data Engine"})
        if response.status_code == 200:
            return response.text
    except Exception:
        return ""
    return ""


def extract_emails(html, website=""):
    emails = set(EMAIL_RE.findall(html or ""))
    valid_emails = []

    for email in emails:
        email = email.lower()
        valid, _ = is_valid_email(email)

        if not valid:
            continue

        # Avoid unrelated third-party technical/vendor emails.
        if email.endswith(".sk") or "gepardfinance" in email:
            continue

        valid_emails.append(email)

    return sorted(valid_emails)


def discover_for_website(website):
    website = str(website).strip()

    if not website or website.lower() == "nan":
        return "", "", "Low", "No website available"

    if not website.startswith(("http://", "https://")):
        website = "https://" + website

    for path in COMMON_PATHS:
        url = urljoin(website, path)
        html = fetch(url)
        emails = extract_emails(html, website)

        if emails:
            return emails[0], url, "Medium", "Auto-discovered public email"

    return "", website, "Low", "No public email found automatically"


def run(limit=25):
    RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)

    batch_file = find_current_email_batch()

    if batch_file is None:
        print("No email batches found.")
        return

    output_file = RESULTS_FOLDER / batch_file.name.replace(".csv", "_interactive_results.csv")

    if output_file.exists():
        df = pd.read_csv(output_file, dtype=str)
    else:
        df = pd.read_csv(batch_file, dtype=str)

    checked = 0
    found = 0

    print("=" * 70)
    print("Auto Email Discovery")
    print("=" * 70)
    print("Batch:", batch_file.name)
    print("Limit:", limit)

    for idx, row in df.iterrows():
        if checked >= limit:
            break

        status = str(row.get("review_status", "")).strip().lower()
        if status in ("email found", "skipped", "no email found"):
            continue

        name = row.get("post_title", "")
        website = row.get("website", "")

        print(f"Checking: {name}")

        email, source, confidence, notes = discover_for_website(website)

        checked += 1

        if email:
            df.at[idx, "suggested_email"] = email
            df.at[idx, "source_url"] = source
            df.at[idx, "confidence"] = confidence
            df.at[idx, "review_status"] = "Auto Email Suggested"
            df.at[idx, "ready_to_merge"] = "No"
            df.at[idx, "notes"] = notes
            found += 1
            print(f"  Found: {email}")
        else:
            df.at[idx, "review_status"] = "Auto No Email Found"
            df.at[idx, "ready_to_merge"] = "No"
            df.at[idx, "notes"] = notes
            print("  No email found")

        df.to_csv(output_file, index=False)

    print("=" * 70)
    print("Auto discovery complete")
    print("Checked:", checked)
    print("Found:", found)
    print("Results:", output_file)


if __name__ == "__main__":
    run()
