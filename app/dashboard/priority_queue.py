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

    priority = df.sort_values("health_score").head(50)

    print()
    print("=" * 75)
    print("203local Priority Queue")
    print("=" * 75)
    print()

    print(
        priority[
            [
                "post_title",
                "town",
                "health_score",
                "website",
                "email",
            ]
        ].to_string(index=False)
    )
