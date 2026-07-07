from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

STATE_FOLDER = ROOT / "automation_state"
REPORT_FOLDER = ROOT / "reports"

STATE_FILE = STATE_FOLDER / "automation_state.json"

DEFAULT_JOB_LIMIT = 5
