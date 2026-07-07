from app.repair_engine.base import RepairModule
from app.schema import fields


class DescriptionRepair(RepairModule):
    module_name = "Description"

    def clean_text(self, value):
        if value is None:
            return ""
        if str(value).lower() == "nan":
            return ""
        return str(value).strip()

    def generate_description(self, row):
        name = self.clean_text(row.get(fields.POST_TITLE))
        town = self.clean_text(row.get(fields.TOWN))
        category = self.clean_text(row.get(fields.PRIMARY_CATEGORY))
        cuisine = self.clean_text(row.get("cuisine_primary"))
        tags = self.clean_text(row.get("post_tags"))

        pieces = []

        if category:
            pieces.append(category)

        if cuisine:
            pieces.append(cuisine)

        descriptor = " and ".join(pieces)

        if town and descriptor:
            return f"{name} is a {descriptor} business located in {town}, Connecticut. It is part of the 203local directory, helping local residents and visitors discover businesses across Fairfield and New Haven County."
        if town:
            return f"{name} is a local business located in {town}, Connecticut. It is part of the 203local directory, helping local residents and visitors discover businesses across Fairfield and New Haven County."
        return f"{name} is part of the 203local directory, helping local residents and visitors discover businesses across Fairfield and New Haven County."

    def run(self, df, dry_run=True):
        report = self.create_report()

        if fields.POST_CONTENT not in df.columns:
            df[fields.POST_CONTENT] = ""

        for index, row in df.iterrows():
            name = self.clean_text(row.get(fields.POST_TITLE))

            if not name:
                report.skipped += 1
                continue

            existing = self.clean_text(row.get(fields.POST_CONTENT))

            if existing:
                report.skipped += 1
                continue

            df.at[index, fields.POST_CONTENT] = self.generate_description(row)
            report.repaired += 1

        return df, report


def run(df, dry_run=True):
    return DescriptionRepair().run(df, dry_run=dry_run)
