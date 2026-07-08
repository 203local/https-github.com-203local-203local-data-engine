from pathlib import Path

from app.orchestrator.history.state_manager import STATE_FILE


def run():
    if STATE_FILE.exists():
        STATE_FILE.unlink()
        print("Enrichment state reset.")
    else:
        print("No enrichment state file found.")
