from abc import ABC, abstractmethod
from app.repair_engine.models import RepairReport


class RepairModule(ABC):
    module_name = "Base Repair"

    def create_report(self):
        return RepairReport(module_name=self.module_name)

    @abstractmethod
    def run(self, df, dry_run=True):
        """
        Run repair logic against a dataframe.

        Must return:
            df, report
        """
        pass
