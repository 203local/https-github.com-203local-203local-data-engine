from pathlib import Path

from app.queue_manager.config import QUEUES
from app.queue_manager.state import load_state


def get_batch_files(batch_folder, pattern):
    folder = Path(batch_folder)

    if not folder.exists():
        return []

    return sorted(folder.glob(pattern))


def get_completed_batches(queue_name):
    state = load_state()
    queue_state = state.get("queues", {}).get(queue_name, {})

    return {
        batch_name
        for batch_name, info in queue_state.items()
        if str(info.get("status", "")).lower() == "complete"
    }


def get_next_batch(queue_name, batch_folder=None, pattern=None):
    if batch_folder is None or pattern is None:
        config = QUEUES.get(queue_name)

        if config is None:
            return None

        batch_folder = config["folder"]
        pattern = config["pattern"]

    batch_files = get_batch_files(batch_folder, pattern)
    completed = get_completed_batches(queue_name)

    for batch_file in batch_files:
        if batch_file.name not in completed:
            return batch_file

    return None


def show_next_batches():
    print("=" * 70)
    print("Queue Manager - Next Batches")
    print("=" * 70)

    for queue_name in sorted(QUEUES.keys()):
        next_batch = get_next_batch(queue_name)

        if next_batch:
            print(f"{queue_name}: {next_batch.name}")
        else:
            print(f"{queue_name}: No unfinished batches found.")


if __name__ == "__main__":
    show_next_batches()
