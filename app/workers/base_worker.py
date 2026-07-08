from dataclasses import dataclass, field


@dataclass
class WorkerUpdate:
    field: str
    value: object
    source: str = ""
    confidence: float = 0.0
    notes: str = ""


@dataclass
class WorkerResult:
    worker_name: str
    business_name: str
    updates: list[WorkerUpdate] = field(default_factory=list)
    status: str = "skipped"
    notes: list[str] = field(default_factory=list)


class BaseWorker:
    name = "Base Worker"

    def can_run(self, row):
        return False

    def run(self, row):
        business_name = str(row.get("post_title", "")).strip()

        return WorkerResult(
            worker_name=self.name,
            business_name=business_name,
            status="skipped",
        )
