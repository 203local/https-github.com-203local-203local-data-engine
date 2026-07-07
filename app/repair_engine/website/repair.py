from app.repair_engine.base import RepairModule
from app.repair_engine.adapters.website_search import build_google_search_url
from app.schema import fields


class WebsiteRepair(RepairModule):
    module_name = "Website"

    def clean_text(self, value):
        if value is None:
            return ""
        if str(value).lower() == "nan":
            return ""
        return str(value).strip()

    def run(self, df, dry_run=True):
        report = self.create_report()

        if fields.WEBSITE not in df.columns:
            df[fields.WEBSITE] = ""

        if fields.WEBSITE_SEARCH_URL not in df.columns:
            df[fields.WEBSITE_SEARCH_URL] = ""

        for index, row in df.iterrows():
            website = self.clean_text(row.get(fields.WEBSITE))
            name = self.clean_text(row.get(fields.POST_TITLE))
            town = self.clean_text(row.get(fields.TOWN))

            if website:
                report.skipped += 1
                continue

            if not name:
                report.skipped += 1
                continue

            df.at[index, fields.WEBSITE_SEARCH_URL] = build_google_search_url(name, town)
            report.repaired += 1

        return df, report


def run(df, dry_run=True):
    return WebsiteRepair().run(df, dry_run=dry_run)
