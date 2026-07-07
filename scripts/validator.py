from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from config import REPORT_FOLDER
from scripts.master_loader import load_master
from scripts.field_dictionary_loader import get_required_fields
from scripts.change_log import log_event
from utils import is_blank, looks_like_email, looks_like_url, normalize_key, timestamp

def find_missing_columns(df, required_fields):
    rows = []
    for col in required_fields:
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
    if not {"post_title", "town"}.issubset(set(df.columns)):
        return pd.DataFrame()
    temp = df.copy()
    temp["_key"] = temp["post_title"].apply(normalize_key) + "|" + temp["town"].apply(normalize_key)
    temp = temp[temp["_key"] != "|"]
    dupes = temp[temp.duplicated("_key", keep=False)].copy()
    if dupes.empty:
        return pd.DataFrame()
    dupes["issue"] = "Possible duplicate business name + town"
    return dupes.drop(columns=["_key"])

def data_quality_score(summary_rows):
    # Simple MVP score: start at 100 and subtract weighted issue ratios.
    total_issues = sum(row["issue_count"] for row in summary_rows if "duplicate" not in row["check"])
    duplicate_issues = sum(row["issue_count"] for row in summary_rows if "duplicate" in row["check"])
    score = 100 - min(45, total_issues * 0.003) - min(15, duplicate_issues * 0.01)
    return round(max(score, 0), 1)

def run_validation():
    print("Running validation...")
    df = load_master(create_backup=True)
    REPORT_FOLDER.mkdir(exist_ok=True)
    required_fields = get_required_fields()

    checks = {
        "missing_required_columns": find_missing_columns(df, required_fields),
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
    priorities = {
        "missing_required_columns": "Critical",
        "missing_business_name": "Critical",
        "duplicate_business_town": "High",
        "duplicate_websites": "High",
        "invalid_websites": "High",
        "invalid_emails": "High",
        "missing_website": "Medium",
        "missing_email": "Medium",
        "missing_phone": "Medium",
    }

    for name, result in checks.items():
        count = 0 if result is None or result.empty else len(result)
        summary_rows.append({
            "check": name,
            "issue_count": count,
            "priority": priorities.get(name, "Review"),
            "recommended_action": "Review / fix records" if count else "No action needed"
        })

    score = data_quality_score(summary_rows)
    dashboard = pd.DataFrame([
        {"metric": "Total businesses", "value": len(df)},
        {"metric": "Total fields", "value": len(df.columns)},
        {"metric": "Data quality score", "value": score},
        {"metric": "Required fields from dictionary", "value": len(required_fields)},
    ])

    report_path = REPORT_FOLDER / f"Validation_Report_{timestamp()}.xlsx"
    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        dashboard.to_excel(writer, sheet_name="Dashboard", index=False)
        pd.DataFrame(summary_rows).to_excel(writer, sheet_name="Summary", index=False)
        for name, result in checks.items():
            if result is not None and not result.empty:
                safe_name = name[:31]
                result.to_excel(writer, sheet_name=safe_name, index=False)

    log_event("Validation", f"Created validation report: {report_path.name}", len(df))
    print("Validation complete.")
    print("Data quality score:", score)
    print("Report created:", report_path)

if __name__ == "__main__":
    run_validation()
