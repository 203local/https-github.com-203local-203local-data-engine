from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

FIELD_DICTIONARY = ROOT / "taxonomy" / "field_dictionary.xlsx"

def load_field_dictionary():
    if not FIELD_DICTIONARY.exists():
        print("Field dictionary not found:", FIELD_DICTIONARY)
        raise SystemExit(1)
    df = pd.read_excel(FIELD_DICTIONARY, sheet_name="Field Dictionary")
    print(f"Loaded field dictionary: {len(df):,} fields")
    return df

def get_website_export_fields():
    df = load_field_dictionary()
    fields = df[df["website_export"].astype(str).str.lower() == "yes"]["column_name"].tolist()
    print(f"Website export fields: {len(fields):,}")
    return fields

def get_required_fields():
    df = load_field_dictionary()
    fields = df[df["required"].astype(str).str.lower() == "yes"]["column_name"].tolist()
    print(f"Required fields: {len(fields):,}")
    return fields

if __name__ == "__main__":
    load_field_dictionary()
    get_required_fields()
    get_website_export_fields()
