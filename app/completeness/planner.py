from dataclasses import dataclass, field

from app.completeness.analyzer import analyze


@dataclass
class RepairPlan:
    current_score: int
    steps: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)

    @property
    def estimated_score_after(self):
        # Simple first estimate: each repair step improves score by 10 points,
        # capped at 100.
        return min(100, self.current_score + (len(self.steps) * 10))


def build_plan(row):
    result = analyze(row)

    return RepairPlan(
        current_score=result.score,
        steps=result.suggested_repairs,
        missing_fields=result.missing_fields,
    )
