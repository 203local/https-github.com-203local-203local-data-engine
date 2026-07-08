from app.orchestrator.engine import run_business
from app.orchestrator.history.logger import log_repair


def execute(row):
    """
    Execute every planned repair for a business.

    Today this marks repairs as executed and logs each repair attempt.

    Future versions will actually invoke:
        Website Repair
        Email Repair
        Google Business Repair
        Restaurant Intelligence
        SEO Repair
        Business Intelligence
    """

    result = run_business(row, execute=True)

    for step in result.executed_steps:
        log_repair(
            result.business_name,
            step,
            status="executed",
        )

    return result
