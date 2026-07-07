import pandas as pd
from config import MASTER_FILE


def is_blank(value):
    return pd.isna(value) or str(value).strip().lower() in {"", "nan", "null", "none"}


def count_filled(df, column):
    if column not in df.columns:
        return 0
    return df[column].apply(lambda x: not is_blank(x)).sum()


def count_blank(df, column):
    if column not in df.columns:
        return 0
    return df[column].apply(is_blank).sum()


def pct(part, total):
    if total == 0:
        return "0.0%"
    return f"{(part / total) * 100:.1f}%"


def looks_like_restaurant(row):
    fields = [
        "primary_category",
        "primary_business_type",
        "business_types",
        "website_directory_category",
    ]

    text = " ".join(str(row.get(field, "")) for field in fields).lower()

    keywords = [
        "restaurant",
        "food",
        "cafe",
        "coffee",
        "bakery",
        "bar",
        "brewery",
        "pizza",
        "deli",
        "market",
        "catering",
        "ice cream",
        "juice",
    ]

    return any(keyword in text for keyword in keywords)


def show_stats():
    df = pd.read_excel(MASTER_FILE, dtype=str)
    total = len(df)

    websites = count_filled(df, "website")
    emails = count_filled(df, "email")
    phones = count_filled(df, "phone")
    descriptions = count_filled(df, "post_content")
    seo_titles = count_filled(df, "seo_directory_title")
    seo_descriptions = count_filled(df, "seo_meta_description")
    restaurant_notes = count_filled(df, "restaurant_intelligence_notes")

    restaurants = df[df.apply(looks_like_restaurant, axis=1)].copy()
    restaurant_total = len(restaurants)
    restaurant_complete = count_filled(restaurants, "restaurant_intelligence_notes")

    print("=" * 70)
    print("203local Data Engine Dashboard")
    print("=" * 70)
    print()
    print(f"Master Businesses:                 {total:,}")
    print()
    print("Website Discovery")
    print("-" * 70)
    print(f"With Website:                      {websites:,} ({pct(websites, total)})")
    print(f"Missing Website:                   {total - websites:,}")
    print()
    print("Email Discovery")
    print("-" * 70)
    print(f"With Email:                        {emails:,} ({pct(emails, total)})")
    print(f"Missing Email:                     {total - emails:,}")
    print()
    print("Core Contact Data")
    print("-" * 70)
    print(f"With Phone:                        {phones:,} ({pct(phones, total)})")
    print(f"Missing Phone:                     {total - phones:,}")
    print()
    print("AI Directory Enrichment")
    print("-" * 70)
    print(f"Descriptions Complete:             {descriptions:,} ({pct(descriptions, total)})")
    print(f"SEO Titles Complete:               {seo_titles:,} ({pct(seo_titles, total)})")
    print(f"SEO Meta Descriptions Complete:    {seo_descriptions:,} ({pct(seo_descriptions, total)})")
    print()
    print("Restaurant Intelligence")
    print("-" * 70)
    print(f"Restaurant/Food Businesses:        {restaurant_total:,}")
    print(f"Restaurant Intelligence Complete:  {restaurant_complete:,} ({pct(restaurant_complete, restaurant_total)})")
    print(f"Restaurant Intelligence Remaining: {restaurant_total - restaurant_complete:,}")
    print()
    print("=" * 70)


if __name__ == "__main__":
    show_stats()
