from app.repair_engine.base import RepairModule


class GoogleBusinessRepair(RepairModule):
    name = "Google Business"

    def repair_row(self, row):
        """
        Placeholder for future Google Business enrichment.

        Planned fields:
        - google_maps_url
        - google_rating
        - google_review_count
        - price_range
        - primary_category verification
        - phone verification
        - website verification
        """
        return row
