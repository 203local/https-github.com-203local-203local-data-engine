import pandas as pd

from app.core.workbook import find_master_workbook


def run():
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    print(f"\nUsing: {workbook}\n")

    df = pd.read_excel(workbook)

    total = len(df)

    print("=" * 75)
    print(f'{"Field":35} {"Missing":>10} {"Complete":>10} {"% Complete":>12}')
    print("=" * 75)

    for column in df.columns:

        missing = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        complete = total - missing
        percent = (complete / total) * 100 if total else 0

        print(
            f"{column[:35]:35}"
            f"{missing:>10}"
            f"{complete:>10}"
            f"{percent:>11.1f}%"
        )

    print("=" * 75)
