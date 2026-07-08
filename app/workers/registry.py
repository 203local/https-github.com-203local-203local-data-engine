from app.workers.base_worker import BaseWorker


class WorkerRegistry:
    def __init__(self):
        self._workers = []

    def register(self, worker):
        self._workers.append(worker)

    def all(self):
        return self._workers

    def runnable(self, row):
        return [w for w in self._workers if w.can_run(row)]


registry = WorkerRegistry()
