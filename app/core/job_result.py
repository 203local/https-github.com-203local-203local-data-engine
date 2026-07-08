from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class JobResult:
    name: str

    repaired: int = 0
    skipped: int = 0
    failed: int = 0

    started_at: datetime = field(default_factory=datetime.now)
    finished_at: Optional[datetime] = None

    notes: list = field(default_factory=list)

    def finish(self):
        self.finished_at = datetime.now()

    @property
    def runtime_seconds(self):
        if self.finished_at is None:
            return 0

        return round(
            (self.finished_at - self.started_at).total_seconds(),
            2,
        )

    def summary(self):
        return {
            "name": self.name,
            "repaired": self.repaired,
            "skipped": self.skipped,
            "failed": self.failed,
            "runtime_seconds": self.runtime_seconds,
        }
