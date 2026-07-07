from app.core.workbook import load_master_dataframe, save_report_workbook
from app.repair_engine.seo.repair import SEORepair


PIPELINE = [
    SEORepair(),
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

    print("\n=== Repair Pipeline Complete ===")
    print(f"Modules run: {len(reports)}")
    print("Saved repaired file to:")
    print(output_path)
