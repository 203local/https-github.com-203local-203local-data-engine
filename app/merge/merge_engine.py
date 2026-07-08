from dataclasses import dataclass, field


@dataclass
class MergeResult:
    accepted_updates: list = field(default_factory=list)
    rejected_updates: list = field(default_factory=list)


def is_empty(value):
    if value is None:
        return True

    value = str(value).strip()

    return value == "" or value.lower() == "nan"


def merge_updates(row, updates):
    result = MergeResult()

    for update in updates:
        current_value = row.get(update.field)

        if is_empty(update.value):
            result.rejected_updates.append(update)
            continue

        if is_empty(current_value):
            result.accepted_updates.append(update)
        else:
            result.rejected_updates.append(update)

    return result
