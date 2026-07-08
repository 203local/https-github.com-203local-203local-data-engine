from app.orchestrator.engine import run_business


def execute(row):
    """
    Execute every planned repair for a business.

    Today this simply marks repairs as executed.

    Future versions will actually invoke:
        Website Repair
        Email Repair
        Google Business Repair
        Restaurant Intelligence
        SEO Repair
        Business Intelligence
    """

    return run_business(row, execute=True)
