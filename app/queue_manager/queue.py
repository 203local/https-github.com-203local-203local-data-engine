from pathlib import Path

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


def get_next_batch(queue_name, batch_folder, pattern):
    batch_files = get_batch_files(batch_folder, pattern)
    completed = get_completed_batches(queue_name)

    for batch_file in batch_files:
        if batch_file.name not in completed:
            return batch_file

    return None


if __name__ == "__main__":
    from app.ai_enrichment.config import BATCH_FOLDER as AI_BATCH_FOLDER

    next_batch = get_next_batch(
        "ai_enrichment",
        AI_BATCH_FOLDER,
        "ai_batch_*.csv",
    )

    if next_batch:
        print("Next batch:", next_batch.name)
    else:
        print("No unfinished batches found.")
