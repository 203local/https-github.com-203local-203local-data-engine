from app.dashboard.summary import show_summary
from app.dashboard.stats import show_stats

from app.jobs.website_discovery.interactive import run as run_website_discovery
from app.jobs.website_discovery.batch_manager import (
    show_batches as show_website_batches,
    find_current_batch as find_current_website_batch,
)
from app.jobs.website_discovery.merge_preview import show_merge_preview as show_website_merge_preview

from app.email_discovery.interactive import run as run_email_discovery
from app.email_discovery.batch_manager import (
    show_batches as show_email_batches,
    find_current_batch as find_current_email_batch,
)
from app.email_discovery.merge_preview import show_merge_preview as show_email_merge_preview
from app.email_discovery.merge import merge_emails
from app.email_discovery.auto_discover import run as run_auto_email_discovery
from app.email_discovery.review_suggestions import review_suggestions

from app.ai_enrichment.batch_manager import show_batches as show_ai_batches
from app.ai_enrichment.auto_enrich import run as run_ai_auto_enrich
from app.ai_enrichment.review_suggestions import review_suggestions as review_ai_suggestions
from app.ai_enrichment.merge_preview import show_merge_preview as show_ai_merge_preview
from app.ai_enrichment.merge import merge_ai_enrichment

from app.restaurant_intelligence.auto_enrich import run as run_restaurant_intelligence
from app.restaurant_intelligence.review_suggestions import review_suggestions as review_restaurant_intelligence
from app.restaurant_intelligence.merge_preview import show_merge_preview as show_restaurant_intelligence_preview
from app.restaurant_intelligence.merge import merge_restaurant_intelligence


def continue_website_discovery():
    batch = find_current_website_batch()

    if batch is None:
        print("No website discovery batches found.")
        return

    print()
    print("Continuing Website Discovery")
    print("Batch:", batch.name)
    print()

    run_website_discovery()


def continue_email_discovery():
    batch = find_current_email_batch()

    if batch is None:
        print("No email discovery batches found.")
        return

    print()
    print("Continuing Email Discovery")
    print("Batch:", batch.name)
    print()

    run_email_discovery()


def menu():
    while True:
        print()
        print("=" * 60)
        print("203local Data Engine v2.2")
        print("=" * 60)
        print("1. Dashboard")
        print("1A. Detailed Stats Dashboard")
        print("2. Continue Website Discovery")
        print("3. Website Batch Manager")
        print("4. Website Merge Preview")
        print("5. Continue Email Discovery")
        print("6. Email Batch Manager")
        print("7. Auto Email Discovery")
        print("8. Review Email Suggestions")
        print("9. Email Merge Preview")
        print("10. Email Merge Manager")
        print("11. AI Batch Manager")
        print("12. Auto AI Enrichment")
        print("13. Review AI Suggestions")
        print("14. AI Merge Preview")
        print("15. AI Merge Manager")
        print("16. Restaurant Intelligence Auto Enrichment")
        print("17. Review Restaurant Intelligence")
        print("18. Restaurant Intelligence Merge Preview")
        print("19. Restaurant Intelligence Merge Manager")
        print("20. Exit")
        print()

        choice = input("Select an option: ").strip()

        if choice == "1":
            show_summary()
        elif choice.lower() == "1a":
            show_stats()
        elif choice == "2":
            continue_website_discovery()
        elif choice == "3":
            show_website_batches()
        elif choice == "4":
            show_website_merge_preview()
        elif choice == "5":
            continue_email_discovery()
        elif choice == "6":
            show_email_batches()
        elif choice == "7":
            run_auto_email_discovery()
        elif choice == "8":
            review_suggestions()
        elif choice == "9":
            show_email_merge_preview()
        elif choice == "10":
            merge_emails()
        elif choice == "11":
            show_ai_batches()
        elif choice == "12":
            run_ai_auto_enrich()
        elif choice == "13":
            review_ai_suggestions()
        elif choice == "14":
            show_ai_merge_preview()
        elif choice == "15":
            merge_ai_enrichment()
        elif choice == "16":
            run_restaurant_intelligence()
        elif choice == "17":
            review_restaurant_intelligence()
        elif choice == "18":
            show_restaurant_intelligence_preview()
        elif choice == "19":
            merge_restaurant_intelligence()
        elif choice == "20":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()
