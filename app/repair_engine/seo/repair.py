import re

from app.repair_engine.base import RepairModule
from app.schema import fields


class SEORepair(RepairModule):
    module_name = "SEO"

    seo_columns = [
        fields.SEO_DIRECTORY_TITLE,
        fields.SEO_META_DESCRIPTION,
        fields.SEARCHABLE_KEYWORDS,
        fields.POST_CONTENT,
    ]

    def clean_text(self, value):
        if value is None:
            return ""
        if str(value).lower() == "nan":
            return ""
        return str(value).strip()

    def slugify(self, text):
        text = self.clean_text(text).lower()
        text = re.sub(r"[^a-z0-9]+", "-", text)
        return text.strip("-")

    def generate_seo_title(self, row):
        name = self.clean_text(row.get(fields.POST_TITLE))
        town = self.clean_text(row.get(fields.TOWN))
        category = self.clean_text(row.get(fields.PRIMARY_CATEGORY))

        if town and category:
            return f"{name} | {category} in {town}, CT"
        if town:
            return f"{name} in {town}, CT"
        return name

    def generate_meta_description(self, row):
        name = self.clean_text(row.get(fields.POST_TITLE))
        town = self.clean_text(row.get(fields.TOWN))
        category = self.clean_text(row.get(fields.PRIMARY_CATEGORY))

        if town and category:
            return f"Find {name}, a {category} business in {town}, CT, in the 203local directory."
        if town:
            return f"Find {name} in {town}, CT, in the 203local directory."
        return f"Find {name} in the 203local directory."

    def generate_keywords(self, row):
        keywords = [
            self.clean_text(row.get(fields.POST_TITLE)),
            self.clean_text(row.get(fields.TOWN)),
            self.clean_text(row.get(fields.COUNTY)),
            self.clean_text(row.get(fields.PRIMARY_CATEGORY)),
            "203local",
            "Connecticut business directory",
        ]

        return ", ".join([k for k in keywords if k])

    def generate_directory_description(self, row):
        name = self.clean_text(row.get(fields.POST_TITLE))
        town = self.clean_text(row.get(fields.TOWN))
        category = self.clean_text(row.get(fields.PRIMARY_CATEGORY))

        if town and category:
            return f"{name} is listed in the 203local directory as a {category} business located in {town}, Connecticut."
        if town:
            return f"{name} is listed in the 203local directory as a business located in {town}, Connecticut."
        return f"{name} is listed in the 203local directory."

    def run(self, df, dry_run=True):
        report = self.create_report()

        for col in self.seo_columns:
            if col not in df.columns:
                df[col] = ""

        for index, row in df.iterrows():
            name = self.clean_text(row.get(fields.POST_TITLE))

            if not name:
                report.skipped += 1
                continue

            changed = False

            if not self.clean_text(row.get(fields.SEO_DIRECTORY_TITLE)):
                df.at[index, fields.SEO_DIRECTORY_TITLE] = self.generate_seo_title(row)
                changed = True

            if not self.clean_text(row.get(fields.SEO_META_DESCRIPTION)):
                df.at[index, fields.SEO_META_DESCRIPTION] = self.generate_meta_description(row)
                changed = True

            if not self.clean_text(row.get(fields.SEARCHABLE_KEYWORDS)):
                df.at[index, fields.SEARCHABLE_KEYWORDS] = self.generate_keywords(row)
                changed = True

            if not self.clean_text(row.get(fields.POST_CONTENT)):
                df.at[index, fields.POST_CONTENT] = self.generate_directory_description(row)
                changed = True

            if changed:
                report.repaired += 1
            else:
                report.skipped += 1

        return df, report


def run(df, dry_run=True):
    return SEORepair().run(df, dry_run=dry_run)
