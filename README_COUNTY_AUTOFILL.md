# 203local Data Engine v0.5 - County Auto-Fill

This update adds a safe enrichment module that fills blank `county` values using:

`reference/ct_towns.csv`

It will:
- Create a backup before editing the master
- Never overwrite an existing county
- Fill only blank county cells when the town has a match
- Save the updated master workbook
- Create a report in the reports folder
- Log the run in logs/change_log.xlsx

Run from the project folder:

```bash
python3 scripts/county_autofill.py
```

Or run:

```bash
python3 main.py
```

and choose option 5.
