import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
STATE_FOLDER = ROOT / "queue_state"
STATE_FILE = STATE_FOLDER / "queue_state.json"


def load_state():
    if not STATE_FILE.exists():
        return {"queues": {}, "runs": []}

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    STATE_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def update_queue_status(queue_name, batch_name, status, details=None):
    state = load_state()

    state["queues"].setdefault(queue_name, {})
    state["queues"][queue_name][batch_name] = {
        "status": status,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "details": details or {},
    }

    save_state(state)


def record_run(queue_name, batch_name, status, details=None):
    state = load_state()

    state["runs"].append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "queue": queue_name,
        "batch": batch_name,
        "status": status,
        "details": details or {},
    })

    save_state(state)
