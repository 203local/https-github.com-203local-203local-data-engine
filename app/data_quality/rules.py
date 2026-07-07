import pandas as pd


def is_blank(value):
    return pd.isna(value) or str(value).strip().lower() in {"", "nan", "null", "none"}


def check_required_fields(row):
    issues = []

    required = ["business_id", "post_title", "town", "county"]

    for field in required:
        if is_blank(row.get(field, "")):
            issues.append(f"Missing required field: {field}")

    return issues


def check_contact_fields(row):
    issues = []

    if is_blank(row.get("phone", "")):
        issues.append("Missing phone")

    if is_blank(row.get("website", "")):
        issues.append("Missing website")

    if is_blank(row.get("email", "")):
        issues.append("Missing email")

    return issues


def check_seo_fields(row):
    issues = []

    if is_blank(row.get("post_content", "")):
        issues.append("Missing description")

    if is_blank(row.get("seo_directory_title", "")):
        issues.append("Missing SEO title")

    if is_blank(row.get("seo_meta_description", "")):
        issues.append("Missing SEO meta description")

    return issues


def check_classification_fields(row):
    issues = []

    if is_blank(row.get("primary_category", "")):
        issues.append("Missing primary category")

    if is_blank(row.get("primary_business_type", "")):
        issues.append("Missing primary business type")

    return issues


def run_quality_rules(row):
    issues = []

    issues.extend(check_required_fields(row))
    issues.extend(check_contact_fields(row))
    issues.extend(check_seo_fields(row))
    issues.extend(check_classification_fields(row))

    return issues
