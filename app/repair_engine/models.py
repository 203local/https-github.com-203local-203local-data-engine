from dataclasses import dataclass, field


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
