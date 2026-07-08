import pandas as pd

from app.scoring.business_score import calculate_health_score


def build_queue(df, minimum_score=90):
    df = df.copy()

    df["health_score"] = df.apply(calculate_health_score, axis=1)

    queue = (
        df[df["health_score"] < minimum_score]
        .sort_values("health_score")
        .reset_index(drop=True)
    )

    return queue
