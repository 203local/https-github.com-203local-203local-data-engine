def business_record_to_text(record):
    fields = [
        "business_id",
        "post_title",
        "town",
        "county",
        "website",
        "primary_category",
        "primary_business_type",
        "business_types",
        "cuisine_primary",
        "cuisines",
        "post_tags",
        "offerings_tags",
        "service_tags",
        "amenities_tags",
    ]

    lines = []

    for field in fields:
        value = record.get(field, "")
        if value and str(value).strip().lower() != "nan":
            lines.append(f"{field}: {value}")

    return "\n".join(lines)
