from pathlib import Path

import pandas as pd


MASTER_FILE = Path("master/203local_Master_Directory.xlsx")

QUEUE_FILES = {
    "Free website crawl": Path("enrichment/website_crawl_queue.csv"),
    "Missing websites": Path("enrichment/missing_website_queue.csv"),
    "Social research": Path("enrichment/missing_website_triage.csv"),
}

FIELD_WEIGHTS = {
    "website": 30,
    "phone": 20,
    "email": 20,
    "facebook": 10,
    "instagram": 10,
    "primary_category": 10,
}


def clean(series):
    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
    )


def completion_count(df, column):
    if column not in df.columns:
        return 0

    return int(clean(df[column]).ne("").sum())


def percentage(value, total):
    if total == 0:
        return 0.0

    return round(value / total * 100, 1)


def queue_count(path):
    if not path.exists():
        return 0

    try:
        return len(pd.read_csv(path))
    except (OSError, pd.errors.ParserError, pd.errors.EmptyDataError):
        return 0


def show_directory_intelligence():
    if not MASTER_FILE.exists():
        print(f"Master workbook not found: {MASTER_FILE}")
        return

    workbook = pd.ExcelFile(MASTER_FILE)
    sheet_name = workbook.sheet_names[0]

    df = pd.read_excel(
        MASTER_FILE,
        sheet_name=sheet_name,
    )

    total = len(df)
    metrics = {}

    for field in FIELD_WEIGHTS:
        complete = completion_count(df, field)
        metrics[field] = {
            "complete": complete,
            "missing": total - complete,
            "percent": percentage(complete, total),
        }

    readiness = sum(
        metrics[field]["percent"] * weight / 100
        for field, weight in FIELD_WEIGHTS.items()
    )

    print()
    print("=" * 72)
    print("203local Directory Intelligence")
    print("=" * 72)
    print()
    print(f"Authoritative workbook: {MASTER_FILE}")
    print(f"Authoritative sheet:    {sheet_name}")
    print(f"Businesses:             {total:,}")
    print()
    print(f"Launch readiness:       {readiness:.1f}%")
    print()

    print("Field Coverage")
    print("-" * 72)

    labels = {
        "website": "Website",
        "phone": "Phone",
        "email": "Email",
        "facebook": "Facebook",
        "instagram": "Instagram",
        "primary_category": "Primary category",
    }

    for field in FIELD_WEIGHTS:
        metric = metrics[field]

        print(
            f"{labels[field]:18} "
            f"{metric['complete']:>6,}/{total:,} "
            f"({metric['percent']:>5.1f}%) "
            f"Missing: {metric['missing']:,}"
        )

    print()
    print("Operational Queues")
    print("-" * 72)

    for label, path in QUEUE_FILES.items():
        print(f"{label:25} {queue_count(path):>6,}")

    triage_file = Path("enrichment/missing_website_triage.csv")

    if triage_file.exists():
        triage = pd.read_csv(triage_file)

        if "research_bucket" in triage.columns:
            print()
            print("Missing Website Research")
            print("-" * 72)

            counts = triage["research_bucket"].value_counts()

            for bucket, count in counts.items():
                print(f"{bucket:35} {count:>6,}")

    if "town" in df.columns and "website" in df.columns:
        missing_websites = df.loc[
            clean(df["website"]).eq("")
        ].copy()

        if not missing_websites.empty:
            top_towns = (
                clean(missing_websites["town"])
                .replace("", "Unknown")
                .value_counts()
                .head(10)
            )

            print()
            print("Top Towns Missing Websites")
            print("-" * 72)

            for town, count in top_towns.items():
                print(f"{town:25} {count:>6,}")

    print()
    print("Cost mode: Free Only")
    print("Paid discovery: Disabled")
    print("AI enrichment: Disabled")
    print()


if __name__ == "__main__":
    show_directory_intelligence()
