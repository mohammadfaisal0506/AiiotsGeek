def adjust_plan(plan: dict, progress: dict):

    for topic in plan.get("topics", []):
        status = progress.get(topic["name"])

        if status == "not_done":
            topic["days"] += 1
            topic["note"] = "Extra day added due to no progress"

        elif status == "partial":
            topic["days"] += 0.5
            topic["note"] = "Half day added for revision"

        elif status == "completed":
            topic["note"] = "On track"

    return plan
