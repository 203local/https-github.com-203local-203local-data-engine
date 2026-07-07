import re
from app.repair_engine.models import RepairReport


SEO_TITLE = "seo_directory_title"
META_DESCRIPTION = "seo_meta_description"
SEARCH_KEYWORDS = "searchable_keywords"
DIRECTORY_DESCRIPTION = "post_content"

BUSINESS_NAME = "post_title"
TOWN = "town"
COUNTY = "county"
CATEGORY = "primary_category"


SEO_COLUMNS = [
    SEO_TITLE,
    META_DESCRIPTION,
    SEARCH_KEYWORDS,
    DIRECTORY_DESCRIPTION,
]


def clean_text(value):
    if value is None:
        return ""
    if str(value).lower() == "nan":
        return ""
    return str(value).strip()


def slugify(text):
    text = clean_text(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def generate_seo_title(row):
    name = clean_text(row.get(BUSINESS_NAME))
    town = clean_text(row.get(TOWN))
    category = clean_text(row.get(CATEGORY))

    if town and category:
        return f"{name} | {category} in {town}, CT"
    if town:
        return f"{name} in {town}, CT"
    return name


def generate_meta_description(row):
    name = clean_text(row.get(BUSINESS_NAME))
    town = clean_text(row.get(TOWN))
    category = clean_text(row.get(CATEGORY))

    if town and category:
        return f"Find {name}, a {category} business in {town}, CT, in the 203local directory."
    if town:
        return f"Find {name} in {town}, CT, in the 203local directory."
    return f"Find {name} in the 203local directory."


def generate_keywords(row):
    name = clean_text(row.get(BUSINESS_NAME))
    town = clean_text(row.get(TOWN))
    county = clean_text(row.get(COUNTY))
    category = clean_text(row.get(CATEGORY))

    keywords = [
        name,
        town,
        county,
        category,
        "203local",
        "Connecticut business directory",
    ]

    return ", ".join([k for k in keywords if k])


def generate_directory_description(row):
    name = clean_text(row.get(BUSINESS_NAME))
    town = clean_text(row.get(TOWN))
    category = clean_text(row.get(CATEGORY))

    if town and category:
        return f"{name} is listed in the 203local directory as a {category} business located in {town}, Connecticut."
    if town:
        return f"{name} is listed in the 203local directory as a business located in {town}, Connecticut."
    return f"{name} is listed in the 203local directory."


def run(df, dry_run=True):
    report = RepairReport(module_name="SEO")

    for col in SEO_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    for index, row in df.iterrows():
        name = clean_text(row.get(BUSINESS_NAME))

        if not name:
            report.skipped += 1
            continue

        changed = False

        if not clean_text(row.get(SEO_TITLE)):
            df.at[index, SEO_TITLE] = generate_seo_title(row)
            changed = True

        if not clean_text(row.get(META_DESCRIPTION)):
            df.at[index, META_DESCRIPTION] = generate_meta_description(row)
            changed = True

        if not clean_text(row.get(SEARCH_KEYWORDS)):
            df.at[index, SEARCH_KEYWORDS] = generate_keywords(row)
            changed = True

        if not clean_text(row.get(DIRECTORY_DESCRIPTION)):
            df.at[index, DIRECTORY_DESCRIPTION] = generate_directory_description(row)
            changed = True

        if changed:
            report.repaired += 1
        else:
            report.skipped += 1

    return df, report
