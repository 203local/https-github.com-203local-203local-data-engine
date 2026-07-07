from pathlib import Path
import pandas as pd
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "enrichment" / "research" / "website_batch_0001.csv"
OUTPUT = ROOT / "enrichment" / "research" / "website_batch_0001_research_template.csv"

df = pd.read_csv(INPUT)

df["google_search_query"] = df.apply(
    lambda r: f'{r["post_title"]} {r["town"]} CT official website',
    axis=1
)

df["google_search_url"] = df["google_search_query"].apply(
    lambda q: "https://www.google.com/search?q=" + quote_plus(q)
)

df["maps_search_query"] = df.apply(
    lambda r: f'{r["post_title"]} {r["town"]} CT',
    axis=1
)

df["official_site_guess"] = ""
df["review_status"] = "Needs Review"
df["ready_to_merge"] = "No"

df.to_csv(OUTPUT, index=False)

print("Research template created:")
print(OUTPUT)
print(f"Rows: {len(df):,}")
