from pathlib import Path
import sys
import pandas as pd
import webbrowser
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.email_discovery.config import RESULTS_FOLDER
from app.email_discovery.batch_manager import find_current_batch


def search_url(name, town):
    query = f"{name} {town} CT email contact official website"
    return "https://www.google.com/search?q=" + quote_plus(query)


def run():
    RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)

    batch_file = find_current_batch()

    if batch_file is None:
        print("No unfinished email batches found.")
        return

    output_file = RESULTS_FOLDER / batch_file.name.replace(
        ".csv",
        "_interactive_results.csv",
    )

    if output_file.exists():
        print("Resuming previous session...")
        df = pd.read_csv(output_file)
    else:
        print("Starting new email batch...")
        df = pd.read_csv(batch_file)

    print("Batch:", batch_file.name)
    print("Results:", output_file)

    for idx, row in df.iterrows():
        status = str(row.get("review_status", "")).strip().lower()

        if status in ("email found", "skipped", "no email found"):
            continue

        name = row.get("post_title", "")
        town = row.get("town", "")
        phone = row.get("phone", "")
        website = row.get("website", "")

        print()
        print("=" * 60)
        print(f"{idx + 1}/{len(df)}")
        print(f"Business: {name}")
        print(f"Town: {town}")
        print(f"Phone: {phone}")
        print(f"Website: {website}")
        print("=" * 60)

        while True:
            print("[G] Open Google Search")
            print("[W] Open Website")
            print("[S] Save Email")
            print("[N] No Email Found")
            print("[K] Skip")
            print("[Q] Quit")

            choice = input("Choose: ").strip().lower()

            if choice == "g":
                webbrowser.open(search_url(name, town))

            elif choice == "w":
                if str(website).strip():
                    webbrowser.open(str(website).strip())
                else:
                    print("No website available.")

            elif choice == "s":
                email = input("Email Address: ").strip()

                source = (
                    input("Source URL (Enter for website): ").strip()
                    or website
                )

                confidence = (
                    input("Confidence (High/Medium/Low): ").strip()
                    or "High"
                )

                df.at[idx, "suggested_email"] = email
                df.at[idx, "source_url"] = source
                df.at[idx, "confidence"] = confidence
                df.at[idx, "review_status"] = "Email Found"
                df.at[idx, "ready_to_merge"] = "Yes"
                df.at[idx, "notes"] = "Interactive Email Discovery"

                df.to_csv(output_file, index=False)

                print("✓ Saved")
                break

            elif choice == "n":
                df.at[idx, "review_status"] = "No Email Found"
                df.at[idx, "ready_to_merge"] = "No"
                df.at[idx, "notes"] = "No public email found"

                df.to_csv(output_file, index=False)

                print("✓ Marked no email found")
                break

            elif choice == "k":
                df.at[idx, "review_status"] = "Skipped"
                df.at[idx, "ready_to_merge"] = "No"

                df.to_csv(output_file, index=False)

                print("✓ Skipped")
                break

            elif choice == "q":
                df.to_csv(output_file, index=False)

                print()
                print("Progress saved.")
                print("Results:", output_file)

                return

            else:
                print("Invalid option.")

    df.to_csv(output_file, index=False)

    print()
    print("=" * 60)
    print("Email Batch Complete!")
    print("=" * 60)
    print("Results saved to:")
    print(output_file)


if __name__ == "__main__":
    run()
