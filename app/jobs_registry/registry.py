from dataclasses import dataclass
from typing import Callable, List


@dataclass
class Job:
    id: str
    name: str
    category: str
    function: Callable
    description: str = ""


JOBS: List[Job] = []


def register_job(job: Job):
    JOBS.append(job)


def get_jobs():
    return JOBS


def get_job_by_id(job_id):
    for job in JOBS:
        if job.id == job_id:
            return job
    return None
