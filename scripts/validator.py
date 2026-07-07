from pathlib import Path
import sys
import pandas as pd
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from config import REPORT_FOLDER, REQUIRED_COLUMNS
from scripts.master_loader import load_master
from utils import is_blank, looks_like_email, looks_like_url, normalize_key, timestamp

def find_missing_columns(df):
    rows = []
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            rows.append({"missing_required_column": col})
    return pd.DataFrame(rows)

def missing_values(df, column):
    if column not in df.columns:
        return pd.DataFrame()
    mask = df[column].apply(is_blank)
    out = df.loc[mask].copy()
    out["issue"] = f"Missing {column}"
    return out

def invalid_emails(df):
    if "email" not in df.columns:
        return pd.DataFrame()
    mask = df["email"].apply(lambda x: not is_blank(x) and not looks_like_email(x))
    out = df.loc[mask].copy()
    out["issue"] = "Invalid email format"
    return out

def invalid_urls(df, column):
    if column not in df.columns:
        return pd.DataFrame()
    mask = df[column].apply(lambda x: not is_blank(x) and not looks_like_url(x))
    out = df.loc[mask].copy()
    out["issue"] = f"Invalid URL format in {column}"
    return out

def duplicate_values(df, column):
    if column not in df.columns:
        return pd.DataFrame()
    temp = df.copy()
    temp["_key"] = temp[column].apply(normalize_key)
    temp = temp[temp["_key"] != ""]
    dupes = temp[temp.duplicated("_key", keep=False)].copy()
    if dupes.empty:
        return pd.DataFrame()
    dupes["issue"] = f"Duplicate {column}"
    return dupes.drop(columns=["_key"])

def duplicate_business_town(df):
    needed = {"post_title", "town"}
    if not needed.issubset(set(df.columns)):
        return pd.DataFrame()
    temp = df.copy()
    temp["_key"] = temp["post_title"].apply(normalize_key) + "|" + temp["town"].apply(normalize_key)
    temp = temp[temp["_key"] != "|"]
    dupes = temp[temp.duplicated("_key", keep=False)].copy()
    if dupes.empty:
        return pd.DataFrame()
    dupes["issue"] = "Possible duplicate business name + town"
    return dupes.drop(columns=["_key"])

def run_validation():
    print("Running validation...")
    df = load_master(create_backup=True)
    REPORT_FOLDER.mkdir(exist_ok=True)

    checks = {
        "missing_required_columns": find_missing_columns(df),
        "missing_business_name": missing_values(df, "post_title"),
        "missing_town": missing_values(df, "town"),
        "missing_county": missing_values(df, "county"),
        "missing_website": missing_values(df, "website"),
        "missing_email": missing_values(df, "email"),
        "missing_phone": missing_values(df, "phone"),
        "missing_primary_category": missing_values(df, "primary_category"),
        "missing_business_type": missing_values(df, "primary_business_type"),
        "invalid_emails": invalid_emails(df),
        "invalid_websites": invalid_urls(df, "website"),
        "invalid_instagram": invalid_urls(df, "instagram"),
        "invalid_facebook": invalid_urls(df, "facebook"),
        "duplicate_business_town": duplicate_business_town(df),
        "duplicate_websites": duplicate_values(df, "website"),
        "duplicate_emails": duplicate_values(df, "email"),
        "duplicate_phones": duplicate_values(df, "phone"),
    }

    summary_rows = []
    for name, result in checks.items():
        count = 0 if result is None or result.empty else len(result)
        summary_rows.append({"check": name, "issue_count": count})

    report_path = REPORT_FOLDER / f"Validation_Report_{timestamp()}.xlsx"
    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        pd.DataFrame(summary_rows).to_excel(writer, sheet_name="Summary", index=False)
        for name, result in checks.items():
            if result is not None and not result.empty:
                safe_name = name[:31]
                result.to_excel(writer, sheet_name=safe_name, index=False)

    print("Validation complete.")
    print("Report created:", report_path)

if __name__ == "__main__":
    run_validation()
