import pandas as pd

from app.core.workbook import find_master_workbook
from app.scoring.business_score import calculate_health_score


def run():
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    df = pd.read_excel(workbook)

    df["health_score"] = df.apply(calculate_health_score, axis=1)

    print()
    print("=" * 70)
    print("203local Business Health Dashboard")
    print("=" * 70)
    print()

    print(
        df[
            ["post_title", "town", "health_score"]
        ]
        .sort_values("health_score")
        .head(25)
        .to_string(index=False)
    )

    print()
    print(f"Average Health Score: {df['health_score'].mean():.1f}/100")
