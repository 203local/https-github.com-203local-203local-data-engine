def apply_updates(df, business_id, accepted_updates):
    mask = df["business_id"] == business_id

    if not mask.any():
        return 0

    applied = 0

    for update in accepted_updates:
        if update.field not in df.columns:
            df[update.field] = ""

        df.loc[mask, update.field] = update.value
        applied += 1

    return applied
