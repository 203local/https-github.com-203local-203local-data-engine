import json
from pathlib import Path

STATE_FILE = Path("logs/enrichment_state.json")


def load_state():
    if not STATE_FILE.exists():
        return {
            "last_business_id": None,
            "completed": 0,
        }

    return json.loads(STATE_FILE.read_text())


def save_state(last_business_id, completed):
    STATE_FILE.parent.mkdir(exist_ok=True)

    STATE_FILE.write_text(
        json.dumps(
            {
                "last_business_id": last_business_id,
                "completed": completed,
            },
            indent=2,
        )
    )
