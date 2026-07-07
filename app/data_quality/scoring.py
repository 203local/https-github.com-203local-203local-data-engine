def score_record(issues):
    score = 100

    penalties = {
        "Missing required field": 25,
        "Missing phone": 10,
        "Missing website": 10,
        "Missing email": 8,
        "Missing description": 10,
        "Missing SEO title": 8,
        "Missing SEO meta description": 8,
        "Missing primary category": 12,
        "Missing primary business type": 12,
    }

    for issue in issues:
        for key, penalty in penalties.items():
            if issue.startswith(key):
                score -= penalty
                break

    return max(score, 0)


def quality_band(score):
    if score >= 95:
        return "Excellent"
    if score >= 80:
        return "Good"
    if score >= 60:
        return "Needs Work"
    return "Poor"
