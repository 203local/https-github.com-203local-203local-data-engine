import json
from datetime import datetime

from app.automation_engine.config import STATE_FILE, STATE_FOLDER


def load_state():
    if not STATE_FILE.exists():
        return {"runs": []}

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    STATE_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def record_run(job_name, status, details=None):
    state = load_state()

    state["runs"].append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "job": job_name,
        "status": status,
        "details": details or {},
    })

    save_state(state)
