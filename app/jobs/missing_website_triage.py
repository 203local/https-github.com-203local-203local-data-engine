from pathlib import Path

import pandas as pd


SOURCE_FILE = Path("enrichment/missing_website_queue.csv")
OUTPUT_FILE = Path("enrichment/missing_website_triage.csv")
SUMMARY_FILE = Path("enrichment/missing_website_triage_summary.csv")


def clean(series):
    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
    )


def valid_social(series):
    values = clean(series)
    lower = values.str.lower()

    invalid = (
        values.eq("")
        | lower.eq("nan")
        | lower.str.endswith("facebook.com/profile.php")
        | lower.str.endswith("facebook.com/profile.php/")
    )

    return ~invalid


def build_triage():
    df = pd.read_csv(SOURCE_FILE)

    phone = clean(df["phone"])
    email = clean(df["email"])
    facebook_valid = valid_social(df["facebook"])
    instagram_valid = valid_social(df["instagram"])

    operating_status = clean(df["operating_status"]).str.lower()
    directory_status = clean(df["directory_status"]).str.lower()

    closure_or_duplicate_signal = (
        operating_status.str.contains(
            r"closed|inactive|duplicate|out of business",
            regex=True,
        )
        | directory_status.str.contains(
            r"closed|inactive|duplicate",
            regex=True,
        )
    )

    has_social = facebook_valid | instagram_valid
    has_direct_contact = phone.ne("") | email.ne("")

    df["has_valid_social"] = has_social
    df["has_phone_or_email"] = has_direct_contact
    df["closure_or_duplicate_signal"] = closure_or_duplicate_signal

    df["research_bucket"] = "Sparse Record"

    df.loc[
        has_direct_contact & ~has_social,
        "research_bucket",
    ] = "Direct Contact Research"

    df.loc[
        has_social,
        "research_bucket",
    ] = "Social-Assisted Research"

    df.loc[
        closure_or_duplicate_signal,
        "research_bucket",
    ] = "Status Review Before Research"

    priority_map = {
        "Status Review Before Research": 1,
        "Social-Assisted Research": 2,
        "Direct Contact Research": 3,
        "Sparse Record": 4,
    }

    df["research_priority"] = (
        df["research_bucket"]
        .map(priority_map)
    )

    df = df.sort_values(
        [
            "research_priority",
            "town",
            "post_title",
        ],
        kind="stable",
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    summary = (
        df["research_bucket"]
        .value_counts()
        .rename_axis("research_bucket")
        .reset_index(name="businesses")
    )

    summary["percent"] = (
        summary["businesses"]
        / len(df)
        * 100
    ).round(1)

    summary.to_csv(
        SUMMARY_FILE,
        index=False,
    )

    print()
    print("=" * 70)
    print("Missing Website Triage")
    print("=" * 70)
    print()
    print(summary.to_string(index=False))
    print()
    print(f"Detailed queue: {OUTPUT_FILE}")
    print(f"Summary: {SUMMARY_FILE}")
    print()
    print("Paid discovery used: No")
    print("AI credits used: $0")


if __name__ == "__main__":
    build_triage()
