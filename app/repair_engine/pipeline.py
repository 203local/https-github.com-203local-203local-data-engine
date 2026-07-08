from app.repair_engine.website.repair import WebsiteRepair
from app.repair_engine.google_business.repair import GoogleBusinessRepair

from app.core.workbook import load_master_dataframe, save_report_workbook

from app.repair_engine.seo.repair import SEORepair
from app.repair_engine.description.repair import DescriptionRepair


PIPELINE = [
    SEORepair(),
    DescriptionRepair(),
    WebsiteRepair(),
    GoogleBusinessRepair(),
]

def run_repair_pipeline():
    print("\n=== Full Repair Pipeline ===")

    try:
        master_path, df = load_master_dataframe()
    except FileNotFoundError as error:
        print(error)
        return

    print(f"Using master file: {master_path}")

    reports = []

    for module in PIPELINE:
        print(f"\nRunning {module.module_name} Repair...")
        df, report = module.run(df)
        report.print_summary()
        reports.append(report)

    output_path = save_report_workbook(
        df=df,
        source_path=master_path,
        suffix="repair_pipeline",
    )

    print("\n====================================")
    print("Repair Pipeline Complete")
    print("====================================")

    for report in reports:
        print(
            f"{report.module_name}: "
            f"Repaired {report.repaired}, "
            f"Skipped {report.skipped}, "
            f"Failed {report.failed}"
        )

    print(f"\nSaved repaired file to:\n{output_path}")
