from app.core.workbook import load_master_dataframe, save_report_workbook
from app.repair_engine.seo.repair import run as run_seo_repair


def run_seo_repair_workflow():
    print("\n=== SEO Auto-Fix ===")

    try:
        master_path, df = load_master_dataframe()
    except FileNotFoundError as error:
        print(error)
        return

    print(f"Using master file: {master_path}")

    df, report = run_seo_repair(df)

    output_path = save_report_workbook(
        df=df,
        source_path=master_path,
        suffix="seo_repaired",
    )

    report.print_summary()

    print("\nSaved repaired file to:")
    print(output_path)
