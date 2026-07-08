
from app.repair_engine.pipeline import run_repair_pipeline
from app.dashboard.profile_snapshot import run as show_profile_snapshot
from app.dashboard.business_health import run as show_business_health
from app.dashboard.priority_queue import run as show_priority_queue
from app.google_business.candidate_report import run as show_google_business_candidates
from app.repair_engine.engine import run_seo_repair_workflow

from app.dashboard.summary import show_summary
from app.dashboard.missing_data import run as show_missing_data
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

from app.business_intelligence.auto_enrich import run as run_business_intelligence
from app.business_intelligence.review_suggestions import review_suggestions as review_business_intelligence
from app.business_intelligence.merge_preview import show_merge_preview as show_business_intelligence_preview
from app.business_intelligence.merge import merge_business_intelligence

from app.automation_engine.runner import show_menu as show_automation_engine
from app.automation_engine.chain_runner import show_menu as show_chain_runner
from app.playbooks.runner import show_menu as show_playbooks

from app.data_quality.audit import run_audit
from app.auto_fix.county_fix import preview_county_fixes
from app.auto_fix.apply import apply_county_fixes


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
        print("203local Data Engine v3.1")
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
        print("20. Business Intelligence Auto Enrichment")
        print("21. Review Business Intelligence")
        print("22. Business Intelligence Merge Preview")
        print("23. Business Intelligence Merge Manager")
        print("24. Automation Engine")
        print("25. Automation Chain Runner")
        print("26. Playbooks")
        print("27. Data Quality Audit")
        print("28. County Auto-Fix Preview")
        print("29. Apply County Auto-Fix")
        print("30. SEO Auto-Fix")
        print("31. Full Repair Pipeline")
        print("32. Missing Data Dashboard")
        print("33. Business Profile Snapshot")
        print("34. Business Health Dashboard")
        print("35. Priority Queue")
        print("36. Google Business Candidate Report")
        print("37. Exit")
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
            run_business_intelligence()
        elif choice == "21":
            review_business_intelligence()
        elif choice == "22":
            show_business_intelligence_preview()
        elif choice == "23":
            merge_business_intelligence()
        elif choice == "24":
            show_automation_engine()
        elif choice == "25":
            show_chain_runner()
        elif choice == "26":
            show_playbooks()
        elif choice == "27":
            run_audit()
        elif choice == "28":
            preview_county_fixes()
        elif choice == "29":
            apply_county_fixes()
        elif choice == "30":
            run_seo_repair_workflow()
        elif choice == "31":
            run_repair_pipeline()
        elif choice == "32":
            show_missing_data()
        elif choice == "33":
            show_profile_snapshot()
        elif choice == "34":
            show_business_health()
        elif choice == "35":
            show_priority_queue()
        elif choice == "36":
            show_google_business_candidates()
        elif choice == "37":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()
