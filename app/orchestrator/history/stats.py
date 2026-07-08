from pathlib import Path
import pandas as pd

from app.orchestrator.history.state_manager import load_state


ERROR_LOG = Path("logs/enrichment_errors.csv")
REPAIR_LOG = Path("logs/repair_history.csv")


def count_rows(path):
    if not path.exists():
        return 0

    try:
        return len(pd.read_csv(path))
    except Exception:
        return 0


def run():
    state = load_state()

    errors = count_rows(ERROR_LOG)
    repairs = count_rows(REPAIR_LOG)

    print()
    print("=" * 70)
    print("203local Enrichment Statistics")
    print("=" * 70)
    print(f"Last business ID:      {state.get('last_business_id')}")
    print(f"Businesses completed:  {state.get('completed')}")
    print()
    print("Logs")
    print("-" * 70)
    print(f"Repair history rows:   {repairs}")
    print(f"Error log rows:        {errors}")
