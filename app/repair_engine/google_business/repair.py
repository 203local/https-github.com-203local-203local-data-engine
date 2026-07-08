from app.repair_engine.base import RepairModule
from app.google_business.mock_provider import MockGoogleBusinessProvider
from app.schema import fields


class GoogleBusinessRepair(RepairModule):
    module_name = "Google Business"

    def __init__(self, provider=None):
        self.provider = provider or MockGoogleBusinessProvider()

    def clean_text(self, value):
        if value is None:
            return ""
        if str(value).lower() == "nan":
            return ""
        return str(value).strip()

    def run(self, df, dry_run=True):
        report = self.create_report()

        for index, row in df.iterrows():
            name = self.clean_text(row.get(fields.POST_TITLE))
            town = self.clean_text(row.get(fields.TOWN))

            if not name:
                report.skipped += 1
                continue

            data = self.provider.search(name, town)

            # Mock provider does not return real data yet.
            # This confirms the module can run safely through the pipeline.
            if data.source == "mock":
                report.skipped += 1
                continue

            report.repaired += 1

        return df, report


def run(df, dry_run=True):
    return GoogleBusinessRepair().run(df, dry_run=dry_run)
