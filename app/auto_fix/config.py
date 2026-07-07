from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

REPORT_FOLDER = ROOT / "reports"

AUTO_FIX_PREVIEW_FILE = REPORT_FOLDER / "Auto_Fix_Preview.csv"
AUTO_FIX_REPORT_FILE = REPORT_FOLDER / "Auto_Fix_Report.csv"

TOWN_TO_COUNTY = {
    # Fairfield County
    "bridgeport": "Fairfield",
    "danbury": "Fairfield",
    "darien": "Fairfield",
    "easton": "Fairfield",
    "fairfield": "Fairfield",
    "greenwich": "Fairfield",
    "monroe": "Fairfield",
    "new canaan": "Fairfield",
    "newtown": "Fairfield",
    "norwalk": "Fairfield",
    "old greenwich": "Fairfield",
    "redding": "Fairfield",
    "ridgefield": "Fairfield",
    "riverside": "Fairfield",
    "sandy hook": "Fairfield",
    "shelton": "Fairfield",
    "sherman": "Fairfield",
    "southport": "Fairfield",
    "stamford": "Fairfield",
    "stratford": "Fairfield",
    "trumbull": "Fairfield",
    "weston": "Fairfield",
    "westport": "Fairfield",
    "wilton": "Fairfield",

    # New Haven County
    "ansonia": "New Haven",
    "beacon falls": "New Haven",
    "bethany": "New Haven",
    "branford": "New Haven",
    "cheshire": "New Haven",
    "derby": "New Haven",
    "east haven": "New Haven",
    "guilford": "New Haven",
    "hamden": "New Haven",
    "madison": "New Haven",
    "meriden": "New Haven",
    "milford": "New Haven",
    "naugatuck": "New Haven",
    "new haven": "New Haven",
    "north branford": "New Haven",
    "north haven": "New Haven",
    "northford": "New Haven",
    "orange": "New Haven",
    "oxford": "New Haven",
    "prospect": "New Haven",
    "seymour": "New Haven",
    "wallingford": "New Haven",
    "waterbury": "New Haven",
    "west haven": "New Haven",
    "woodbridge": "New Haven",
    "yalesville": "New Haven",
}
