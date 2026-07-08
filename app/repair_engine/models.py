from dataclasses import dataclass, field

from app.core.job_result import JobResult


@dataclass
class RepairReport:
    module_name: str
    repaired: int = 0
    skipped: int = 0
    failed: int = 0
    warnings: list[str] = field(default_factory=list)

    def print_summary(self):
        print(f"\n=== {self.module_name} Repair Summary ===")
        print(f"Repaired: {self.repaired}")
        print(f"Skipped: {self.skipped}")
        print(f"Failed: {self.failed}")

        if self.warnings:
            print("\nWarnings:")
            for warning in self.warnings:
                print(f"- {warning}")

    def to_job_result(self):
        result = JobResult(
            name=f"{self.module_name} Repair",
            repaired=self.repaired,
            skipped=self.skipped,
            failed=self.failed,
            notes=self.warnings,
        )
        result.finish()
        return result
