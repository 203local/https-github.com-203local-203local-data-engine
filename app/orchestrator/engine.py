from dataclasses import dataclass, field

from app.completeness.planner import build_plan


@dataclass
class OrchestratorResult:
    business_name: str
    current_score: int
    estimated_score_after: int
    steps: list[str] = field(default_factory=list)
    executed_steps: list[str] = field(default_factory=list)
    skipped_steps: list[str] = field(default_factory=list)


def run_business(row, execute=False):
    plan = build_plan(row)

    business_name = str(row.get("post_title", "")).strip()

    result = OrchestratorResult(
        business_name=business_name,
        current_score=plan.current_score,
        estimated_score_after=plan.estimated_score_after,
        steps=plan.steps,
    )

    for step in plan.steps:
        if execute:
            # Future version will call real repair modules here.
            result.executed_steps.append(step)
        else:
            result.skipped_steps.append(step)

    return result
