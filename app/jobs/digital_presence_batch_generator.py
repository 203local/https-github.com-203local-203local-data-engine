from pathlib import Path
import re

import pandas as pd


MASTER_PATH = Path("master/203local_Master_Directory.xlsx")
OUTPUT_DIR = Path("enrichment/missing_website_batches")
DEFAULT_BATCH_SIZE = 25


def clean(value):
    if value is None:
        return ""

    value = str(value).strip()

    if value.lower() == "nan":
        return ""

    return value


def slugify(value):
    value = clean(value).lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def reviewed_business_ids():
    reviewed = set()

    if not OUTPUT_DIR.exists():
        return reviewed

    for path in OUTPUT_DIR.glob("*.csv"):
        if path.name.endswith("_test.csv"):
            continue

        try:
            df = pd.read_csv(path, dtype=str).fillna("")
        except Exception:
            continue

        if "business_id" not in df.columns:
            continue

        if "research_status" not in df.columns:
            continue

        statuses = (
            df["research_status"]
            .astype(str)
            .str.strip()
            .str.casefold()
        )

        complete_mask = ~statuses.isin(
            {
                "",
                "pending",
                "needs review",
            }
        )

        reviewed.update(
            df.loc[complete_mask, "business_id"]
            .astype(str)
            .str.strip()
            .tolist()
        )

    return reviewed


def prepare_rows(master, town):
    town_mask = (
        master["town"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
        .eq(town.casefold())
    )

    website_missing = (
        master["website"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
    )

    rows = master.loc[town_mask & website_missing].copy()

    already_reviewed = reviewed_business_ids()

    rows = rows[
        ~rows["business_id"]
        .astype(str)
        .str.strip()
        .isin(already_reviewed)
    ].copy()

    required_columns = [
        "business_id",
        "post_title",
        "town",
        "street",
        "phone",
        "email",
        "facebook",
        "instagram",
    ]

    for column in required_columns:
        if column not in rows.columns:
            rows[column] = ""

    rows = rows[required_columns].copy()

    rows["research_status"] = ""
    rows["discovered_website"] = ""
    rows["website_source"] = ""
    rows["website_confidence"] = ""
    rows["research_notes"] = ""
    rows["discovered_primary_online_presence"] = ""
    rows["discovered_online_presence_type"] = ""
    rows["discovered_website_status"] = ""

    return rows


def generate_batches(town, batch_size=DEFAULT_BATCH_SIZE):
    if not MASTER_PATH.exists():
        raise FileNotFoundError(
            f"Master workbook not found: {MASTER_PATH}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    master = pd.read_excel(
        MASTER_PATH,
        dtype=str,
    ).fillna("")

    rows = prepare_rows(master, town)

    print()
    print("=" * 72)
    print("203local Digital Presence Batch Generator")
    print("=" * 72)
    print(f"Town:                    {town}")
    print(f"Missing website records: {len(rows)}")
    print(f"Batch size:              {batch_size}")
    print()

    if rows.empty:
        print("No new businesses need digital presence review.")
        return

    town_slug = slugify(town)

    existing = sorted(
        OUTPUT_DIR.glob(
            f"{town_slug}_digital_presence_batch_*.csv"
        )
    )

    next_number = 1

    if existing:
        numbers = []

        for path in existing:
            match = re.search(
                r"_batch_(\d+)\.csv$",
                path.name,
            )

            if match:
                numbers.append(int(match.group(1)))

        if numbers:
            next_number = max(numbers) + 1

    created = []

    for offset in range(0, len(rows), batch_size):
        batch = rows.iloc[
            offset : offset + batch_size
        ].copy()

        batch_number = next_number + len(created)

        output_path = OUTPUT_DIR / (
            f"{town_slug}_digital_presence_"
            f"batch_{batch_number:03d}.csv"
        )

        batch.to_csv(output_path, index=False)
        created.append(output_path)

    print("Created batches:")
    print("-" * 72)

    for path in created:
        count = len(pd.read_csv(path, dtype=str))
        print(f"{path.name:<55} {count:>3} businesses")

    print()
    print(f"Total batches created: {len(created)}")


def run():
    town = input("Town to generate batches for: ").strip()

    if not town:
        print("No town entered.")
        return

    batch_size_value = input(
        f"Batch size [{DEFAULT_BATCH_SIZE}]: "
    ).strip()

    if batch_size_value:
        try:
            batch_size = int(batch_size_value)
        except ValueError:
            print("Batch size must be a whole number.")
            return
    else:
        batch_size = DEFAULT_BATCH_SIZE

    if batch_size <= 0:
        print("Batch size must be greater than zero.")
        return

    generate_batches(
        town=town,
        batch_size=batch_size,
    )


if __name__ == "__main__":
    run()
