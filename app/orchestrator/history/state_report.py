from app.orchestrator.history.state_manager import load_state


def run():
    state = load_state()

    print()
    print("=" * 60)
    print("Enrichment State")
    print("=" * 60)
    print(f"Last business ID: {state.get('last_business_id')}")
    print(f"Completed:        {state.get('completed')}")
