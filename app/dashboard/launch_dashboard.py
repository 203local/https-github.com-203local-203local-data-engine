from pathlib import Path
import pandas as pd


MASTER_FILE = Path("master/203local_Master_Directory.xlsx")


def pct(value, total):
    return 0 if total == 0 else round(value / total * 100, 1)


def show_launch_dashboard():
    xls = pd.ExcelFile(MASTER_FILE)

    print(f"Using worksheet: {xls.sheet_names[0]}")

    df = pd.read_excel(
        MASTER_FILE,
        sheet_name=xls.sheet_names[0],
    )

    total = len(df)

    def complete(column):
        if column not in df.columns:
            return 0
        return (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .ne("")
            .sum()
        )

    website = complete("website")
    phone = complete("phone")
    email = complete("email")
    facebook = complete("facebook")
    instagram = complete("instagram")

    print()
    print("=" * 60)
    print("203local Launch Dashboard")
    print("=" * 60)
    print()

    print(f"Businesses: {total:,}")
    print()

    print(f"Website:   {website:,}/{total:,} ({pct(website,total)}%)")
    print(f"Phone:     {phone:,}/{total:,} ({pct(phone,total)}%)")
    print(f"Email:     {email:,}/{total:,} ({pct(email,total)}%)")
    print(f"Facebook:  {facebook:,}/{total:,} ({pct(facebook,total)}%)")
    print(f"Instagram: {instagram:,}/{total:,} ({pct(instagram,total)}%)")

