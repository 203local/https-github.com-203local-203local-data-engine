from pathlib import Path

import pandas as pd


MASTER_FILE = Path("master/203local_Master_Directory.xlsx")
OUTPUT_FILE = Path("enrichment/website_crawl_queue.csv")


def clean_series(series):
    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
    )


def build_queue():
    xls = pd.ExcelFile(MASTER_FILE)
    sheet_name = xls.sheet_names[0]

    df = pd.read_excel(
        MASTER_FILE,
        sheet_name=sheet_name,
    )

    required_columns = [
        "business_id",
        "post_title",
        "town",
        "street",
        "website",
        "phone",
        "email",
        "facebook",
        "instagram",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    website = clean_series(df["website"])
    phone = clean_series(df["phone"])
    email = clean_series(df["email"])
    facebook = clean_series(df["facebook"])
    instagram = clean_series(df["instagram"])

    has_website = website.ne("")

    missing_contact_data = (
        phone.eq("")
        | email.eq("")
        | facebook.eq("")
        | instagram.eq("")
    )

    queue = df.loc[
        has_website & missing_contact_data,
        required_columns,
    ].copy()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    queue.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print()
    print("=" * 60)
    print("Free Website Crawl Queue")
    print("=" * 60)
    print()
    print(f"Worksheet: {sheet_name}")
    print(f"Businesses in queue: {len(queue):,}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_queue()
