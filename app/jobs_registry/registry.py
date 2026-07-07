from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class Job:
    id: str
    name: str
    category: str
    function: Callable
    description: str = ""
    estimated_runtime: str = ""
    enabled: bool = True


JOBS: List[Job] = []


def register_job(job: Job):
    JOBS.append(job)


def get_jobs(include_disabled=False):
    if include_disabled:
        return JOBS

    return [job for job in JOBS if job.enabled]


def get_job_by_id(job_id):
    for job in JOBS:
        if job.id == job_id:
            return job
    return None
