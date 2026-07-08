import traceback


def run_worker(worker, row):
    try:
        return worker.run(row), None

    except Exception as exc:
        return None, {
            "worker": worker.name,
            "business_id": row.get("business_id"),
            "business_name": row.get("post_title"),
            "town": row.get("town"),
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }
