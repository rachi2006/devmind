def analyze_activity(events):

    total_events = len(events)

    push_events = 0
    total_commits = 0

    active_repositories = set()
    active_days = set()

    for event in events:

        # Event date
        created_at = event.get("created_at", "")

        if created_at:
            active_days.add(
                created_at[:10]
            )

        # Push event
        if event.get("type") == "PushEvent":

            push_events += 1

            repo_name = event.get(
                "repo", {}
            ).get(
                "name"
            )

            if repo_name:
                active_repositories.add(
                    repo_name
                )

            commits = event.get(
                "payload", {}
            ).get(
                "commits", []
            )

            total_commits += len(
                commits
            )


    # Activity score
    activity_score = min(
        100,
        (
            total_commits * 5
            + len(active_days) * 4
            + len(active_repositories) * 3
        )
    )


    # Consistency level
    if len(active_days) >= 15:
        consistency = "Excellent"

    elif len(active_days) >= 8:
        consistency = "Good"

    elif len(active_days) >= 4:
        consistency = "Moderate"

    else:
        consistency = "Low"


    return {

        "total_events": total_events,

        "push_events": push_events,

        "recent_commits": total_commits,

        "active_days": len(
            active_days
        ),

        "active_repositories": len(
            active_repositories
        ),

        "activity_score": round(
            activity_score
        ),

        "consistency": consistency
    }