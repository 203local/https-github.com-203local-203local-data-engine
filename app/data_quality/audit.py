from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE
from app.data_quality.config import QUALITY_REPORT_FILE, REPORT_FOLDER
from app.data_quality.rules import run_quality_rules
from app.data_quality.scoring import score_record, quality_band


def run_audit():
    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

    master = pd.read_excel(MASTER_FILE, dtype=str)

    rows = []

    for _, row in master.iterrows():
        issues = run_quality_rules(row)
        score = score_record(issues)

        rows.append({
            "business_id": row.get("business_id", ""),
            "post_title": row.get("post_title", ""),
            "town": row.get("town", ""),
            "county": row.get("county", ""),
            "quality_score": score,
            "quality_band": quality_band(score),
            "issue_count": len(issues),
            "issues": " | ".join(issues),
        })

    report = pd.DataFrame(rows)
    report.to_csv(QUALITY_REPORT_FILE, index=False)

    print("=" * 70)
    print("Data Quality Audit Complete")
    print("=" * 70)
    print("Businesses audited:", len(report))
    print("Report:", QUALITY_REPORT_FILE)
    print()
    print(report["quality_band"].value_counts().to_string())


if __name__ == "__main__":
    run_audit()
