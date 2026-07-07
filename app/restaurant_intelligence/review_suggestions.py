from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.restaurant_intelligence.config import RESULTS_FOLDER


def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_results.csv"))
    if not files:
        print("No restaurant intelligence results files found.")
        return None
    return files[-1]


def review_suggestions():
    results_file = latest_results_file()
    if results_file is None:
        return

    df = pd.read_csv(results_file, dtype=str)

    suggestions = df[
        df["review_status"].fillna("").str.lower().eq("restaurant intelligence suggested")
    ]

    if suggestions.empty:
        print("No restaurant intelligence suggestions to review.")
        return

    for idx, row in suggestions.iterrows():
        print("=" * 80)
        print("Business:", row.get("post_title", ""))
        print("Town:", row.get("town", ""))
        print("Website:", row.get("website", ""))
        print("-" * 80)
        print("Cuisine Primary:", row.get("suggested_cuisine_primary", ""))
        print("Cuisines:", row.get("suggested_cuisines", ""))
        print("Service Models:", row.get("suggested_service_model_tags", ""))
        print("Offerings:", row.get("suggested_offerings_tags", ""))
        print("Amenities:", row.get("suggested_amenities_tags", ""))
        print("Dietary:", row.get("suggested_dietary_tags", ""))
        print("Price Range:", row.get("suggested_price_range", ""))
        print("Menu Link:", row.get("suggested_has_menu_link", ""))
        print("Online Ordering:", row.get("suggested_offers_online_ordering", ""))
        print("Takeout:", row.get("suggested_offers_takeout", ""))
        print("Delivery:", row.get("suggested_offers_delivery", ""))
        print("Catering:", row.get("suggested_offers_catering", ""))
        print("Brunch:", row.get("suggested_has_brunch", ""))
        print("Outdoor Dining:", row.get("suggested_outdoor_dining_signal", ""))
        print("-" * 80)
        print("Confidence:", row.get("confidence", ""))
        print("Notes:", row.get("suggested_restaurant_intelligence_notes", "") or row.get("notes", ""))
        print("=" * 80)

        choice = input("[A] Approve  [R] Reject  [S] Skip  [Q] Quit: ").strip().lower()

        if choice == "a":
            df.at[idx, "review_status"] = "Approved"
            df.at[idx, "ready_to_merge"] = "Yes"
            print("✓ Approved")
        elif choice == "r":
            df.at[idx, "review_status"] = "Rejected"
            df.at[idx, "ready_to_merge"] = "No"
            print("✓ Rejected")
        elif choice == "s":
            df.at[idx, "review_status"] = "Skipped"
            df.at[idx, "ready_to_merge"] = "No"
            print("✓ Skipped")
        elif choice == "q":
            df.to_csv(results_file, index=False)
            print("Progress saved.")
            return
        else:
            print("Invalid option; skipped.")

        df.to_csv(results_file, index=False)

    print("Restaurant intelligence review complete.")
    print("Results:", results_file)


if __name__ == "__main__":
    review_suggestions()
