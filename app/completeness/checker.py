from dataclasses import dataclass


@dataclass
class CompletenessResult:
    score: int
    missing_fields: list[str]
    suggested_repairs: list[str]
