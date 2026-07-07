from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from config import FIELD_DICTIONARY_FILE, REQUIRED_COLUMNS
from utils import yes

EXPECTED_COLUMNS = [
    "field_name",
    "required",
    "website_export",
    "crm_field",
    "internal_only",
    "searchable",
    "dropdown",
    "ai_generated",
    "verification_rule",
]

def load_field_dictionary():
    if not FIELD_DICTIONARY_FILE.exists():
        print("Field dictionary not found. Using fallback required fields.")
        return pd.DataFrame({
            "field_name": REQUIRED_COLUMNS,
            "required": ["Yes"] * len(REQUIRED_COLUMNS),
            "website_export": ["Yes"] * len(REQUIRED_COLUMNS),
        })

    df = pd.read_excel(FIELD_DICTIONARY_FILE)
    df.columns = [str(c).strip().lower() for c in df.columns]

    if "field_name" not in df.columns:
        raise ValueError("Field dictionary must include a 'field_name' column.")

    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df["field_name"] = df["field_name"].astype(str).str.strip()
    df = df[df["field_name"] != ""].copy()
    return df

def get_required_fields():
    df = load_field_dictionary()
    if "required" not in df.columns:
        return REQUIRED_COLUMNS
    fields = df[df["required"].apply(yes)]["field_name"].tolist()
    return fields or REQUIRED_COLUMNS

def get_website_export_fields():
    df = load_field_dictionary()
    if "website_export" not in df.columns:
        return []
    return df[df["website_export"].apply(yes)]["field_name"].tolist()

if __name__ == "__main__":
    d = load_field_dictionary()
    print(f"Loaded field dictionary: {len(d)} fields")
    print(f"Required fields: {len(get_required_fields())}")
    print(f"Website export fields: {len(get_website_export_fields())}")
