from app.core.url_classifier import classify_url

from pathlib import Path
from urllib.parse import quote_plus, urlparse
import sys
import webbrowser

import pandas as pd


DEFAULT_BATCH = Path(
    "enrichment/missing_website_batches/"
    "bridgeport_social_batch_001.csv"
)

NON_OFFICIAL_DOMAINS = {
    "facebook.com",
    "www.facebook.com",
    "instagram.com",
    "www.instagram.com",
    "tiktok.com",
    "www.tiktok.com",
    "linktr.ee",
    "www.linktr.ee",
    "places.singleplatform.com",
    "singleplatform.com",
    "www.singleplatform.com",
    "mappway.com",
    "www.mappway.com",
    "yelp.com",
    "www.yelp.com",
    "tripadvisor.com",
    "www.tripadvisor.com",
    "doordash.com",
    "www.doordash.com",
    "grubhub.com",
    "www.grubhub.com",
    "ubereats.com",
    "www.ubereats.com",
}


def clean(value):
    if value is None:
        return ""

    value = str(value).strip()

    if value.lower() == "nan":
        return ""

    return value


def valid_url(value):
    value = clean(value)

    try:
        parsed = urlparse(value)

        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
        )
    except ValueError:
        return False


def is_social_url(value):
    try:
        hostname = (
            urlparse(clean(value))
            .netloc
            .lower()
            .split(":")[0]
        )

        return any(
            hostname == domain
            or hostname.endswith("." + domain)
            for domain in NON_OFFICIAL_DOMAINS
        )
    except ValueError:
        return False


def save_batch(df, batch_path):
    df.to_csv(
        batch_path,
        index=False,
    )


def ensure_columns(df):
    required_columns = [
        "business_id",
        "post_title",
        "research_status",
        "discovered_website",
        "website_source",
        "website_confidence",
        "research_notes",
        "discovered_primary_online_presence",
        "discovered_online_presence_type",
        "discovered_website_status",
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = ""

    return df


def show_business(row, position, total):
    print()
    print("=" * 72)
    print(f"Digital Presence Review — {position} of {total}")
    print("=" * 72)
    print()
    print(f"Business:  {clean(row.get('post_title'))}")
    print(f"Town:      {clean(row.get('town'))}")
    print(f"Address:   {clean(row.get('street'))}")
    print(f"Phone:     {clean(row.get('phone'))}")
    print(f"Email:     {clean(row.get('email'))}")
    print()
    print(
        f"Facebook:  "
        f"{clean(row.get('facebook')) or '(none)'}"
    )
    print(
        f"Instagram: "
        f"{clean(row.get('instagram')) or '(none)'}"
    )
    print()
    print(
        "Current status: "
        f"{clean(row.get('research_status')) or 'Pending'}"
    )
    print()


def set_social_only(
    df,
    index,
    url,
    presence_type,
):
    df.at[index, "research_status"] = "Social Only"
    df.at[index, "discovered_website"] = ""
    df.at[index, "website_source"] = ""
    df.at[index, "website_confidence"] = ""

    df.at[
        index,
        "discovered_primary_online_presence",
    ] = url

    df.at[
        index,
        "discovered_online_presence_type",
    ] = presence_type

    df.at[
        index,
        "discovered_website_status",
    ] = f"{presence_type} Only"

    df.at[
        index,
        "research_notes",
    ] = (
        f"Active {presence_type}. "
        "No official website confirmed."
    )


def review_batch(batch_path=DEFAULT_BATCH):
    batch_path = Path(batch_path)

    if not batch_path.exists():
        raise FileNotFoundError(
            f"Research batch not found: {batch_path}"
        )

    df = pd.read_csv(
        batch_path,
        dtype=str,
    ).fillna("")

    df = ensure_columns(df)

    pending_mask = (
        df["research_status"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
        .isin(
            {
                "",
                "pending",
                "needs review",
            }
        )
    )

    pending_indices = df.index[pending_mask].tolist()

    if not pending_indices:
        print("No pending businesses remain in this batch.")
        return

    print()
    print("=" * 72)
    print("203local Digital Presence Review")
    print("=" * 72)
    print(f"Batch:              {batch_path}")
    print(f"Pending businesses: {len(pending_indices)}")
    print()
    print("This tool changes only the research CSV.")
    print("It does not modify the master workbook.")

    for position, index in enumerate(
        pending_indices,
        start=1,
    ):
        while True:
            row = df.loc[index]

            show_business(
                row,
                position,
                len(pending_indices),
            )

            print("1. Official website found")
            print("2. Open Facebook")
            print("3. Open Instagram")
            print("4. Open Google Search")
            print("5. Open Google Maps search")
            print("6. Facebook is primary presence")
            print("7. Instagram is primary presence")
            print("8. No online presence found")
            print("9. Needs further research")
            print("10. Skip for now")
            print("11. Quit and save")
            print()

            choice = input("Select an option: ").strip()

            if choice == "1":
                website = input(
                    "Official website URL: "
                ).strip()

                classification = classify_url(website)

                print()
                print("=" * 60)
                print("URL Classification")
                print("=" * 60)
                print(
                    f"Category:   "
                    f"{classification.category}"
                )
                print(
                    f"Provider:   "
                    f"{classification.provider}"
                )
                print(
                    f"Confidence: "
                    f"{classification.confidence}"
                )

                if classification.warning:
                    print()
                    print("WARNING")
                    print(classification.warning)

                if classification.category != "official":
                    print()
                    print(
                        "This URL cannot be saved as an "
                        "official website."
                    )
                    print(
                        f"Detected as: "
                        f"{classification.category}"
                    )

                    if classification.provider:
                        print(
                            f"Provider: "
                            f"{classification.provider}"
                        )

                    print()
                    print(
                        "Use the appropriate social-presence "
                        "option or continue researching."
                    )
                    continue

                if not valid_url(website):
                    print(
                        "Invalid URL. Include "
                        "http:// or https://"
                    )
                    continue

                source = input(
                    "Source "
                    "(Facebook/Instagram/Google/Other): "
                ).strip()

                confidence = input(
                    "Confidence (High/Medium/Low): "
                ).strip()

                notes = input(
                    "Notes (optional): "
                ).strip()

                df.at[
                    index,
                    "research_status",
                ] = "Approved"

                df.at[
                    index,
                    "discovered_website",
                ] = classification.canonical_url

                df.at[
                    index,
                    "website_source",
                ] = source

                df.at[
                    index,
                    "website_confidence",
                ] = confidence

                df.at[
                    index,
                    "research_notes",
                ] = notes

                save_batch(df, batch_path)

                print(
                    "Official website approved and saved."
                )
                break

            if choice == "2":
                facebook = clean(row.get("facebook"))

                if facebook:
                    webbrowser.open(facebook)
                    print("Opened Facebook.")
                else:
                    print("No Facebook URL is available.")

                continue

            if choice == "3":
                instagram = clean(row.get("instagram"))

                if instagram:
                    webbrowser.open(instagram)
                    print("Opened Instagram.")
                else:
                    print("No Instagram URL is available.")

                continue

            if choice == "4":
                query = quote_plus(
                    " ".join(
                        value
                        for value in [
                            clean(row.get("post_title")),
                            clean(row.get("town")),
                            "CT official website",
                        ]
                        if value
                    )
                )

                webbrowser.open(
                    f"https://www.google.com/search?q={query}"
                )

                print("Opened Google Search.")
                continue

            if choice == "5":
                query = quote_plus(
                    " ".join(
                        value
                        for value in [
                            clean(row.get("post_title")),
                            clean(row.get("street")),
                            clean(row.get("town")),
                            "CT",
                        ]
                        if value
                    )
                )

                webbrowser.open(
                    "https://www.google.com/maps/"
                    f"search/?api=1&query={query}"
                )

                print("Opened Google Maps search.")
                continue

            if choice == "6":
                facebook = clean(row.get("facebook"))

                if not facebook:
                    print("No Facebook URL is available.")
                    continue

                set_social_only(
                    df,
                    index,
                    facebook,
                    "Facebook",
                )

                save_batch(df, batch_path)

                print(
                    "Saved Facebook as the primary "
                    "online presence."
                )
                break

            if choice == "7":
                instagram = clean(row.get("instagram"))

                if not instagram:
                    print("No Instagram URL is available.")
                    continue

                set_social_only(
                    df,
                    index,
                    instagram,
                    "Instagram",
                )

                save_batch(df, batch_path)

                print(
                    "Saved Instagram as the primary "
                    "online presence."
                )
                break

            if choice == "8":
                notes = input(
                    "Notes or evidence (optional): "
                ).strip()

                df.at[
                    index,
                    "research_status",
                ] = "No Online Presence"

                df.at[
                    index,
                    "discovered_website",
                ] = ""

                df.at[
                    index,
                    "discovered_primary_online_presence",
                ] = ""

                df.at[
                    index,
                    "discovered_online_presence_type",
                ] = "None"

                df.at[
                    index,
                    "discovered_website_status",
                ] = "No Online Presence"

                df.at[
                    index,
                    "research_notes",
                ] = notes

                save_batch(df, batch_path)

                print("Marked as no online presence.")
                break

            if choice == "9":
                notes = input(
                    "What needs further research? "
                ).strip()

                df.at[
                    index,
                    "research_status",
                ] = "Needs Further Research"

                df.at[
                    index,
                    "research_notes",
                ] = notes

                save_batch(df, batch_path)

                print("Marked for further research.")
                break

            if choice == "10":
                print("Skipped. It remains pending.")
                break

            if choice == "11":
                save_batch(df, batch_path)
                print(f"Saved: {batch_path}")
                return

            print("Please enter a number from 1 through 11.")

    save_batch(df, batch_path)

    print()
    print("=" * 72)
    print("Digital Presence Review Complete")
    print("=" * 72)
    print(f"Saved batch: {batch_path}")
    print()

    status_counts = (
        df["research_status"]
        .replace("", "Pending")
        .value_counts()
    )

    print(status_counts.to_string())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        review_batch(sys.argv[1])
    else:
        review_batch()
