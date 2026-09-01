def calculate_readiness_score(
    completion_percentage,
    skill_analysis,
    github_data,
    developer_weaknesses
):

    # -------------------------
    # 1. PROFILE SCORE
    # Maximum: 20 points
    # -------------------------

    profile_score = (
        completion_percentage / 100
    ) * 20


    # -------------------------
    # 2. SKILL SCORE
    # Maximum: 25 points
    # -------------------------

    if skill_analysis:

        total_skill_score = sum(
            item.get("score", 0)
            for item in skill_analysis
        )

        average_skill_score = (
            total_skill_score /
            len(skill_analysis)
        )

    else:

        average_skill_score = 0


    skill_score = (
        average_skill_score / 100
    ) * 25


    # -------------------------
    # 3. GITHUB ACTIVITY
    # Maximum: 20 points
    # -------------------------

    activity_score = github_data.get(
        "activity_score",
        0
    )

    activity_score = min(
        max(activity_score, 0),
        100
    )

    github_activity_points = (
        activity_score / 100
    ) * 20


    # -------------------------
    # 4. PROJECT PORTFOLIO
    # Maximum: 20 points
    # -------------------------

    public_repos = github_data.get(
        "public_repos",
        0
    )

    # 10 or more repositories = full score

    repository_score = min(
        public_repos / 10,
        1
    ) * 20


    # -------------------------
    # 5. DEVELOPER GAPS
    # Maximum: 15 points
    # -------------------------

    high_priority_gaps = sum(
        1
        for weakness in developer_weaknesses
        if weakness.get("priority") == "High"
    )

    medium_priority_gaps = sum(
        1
        for weakness in developer_weaknesses
        if weakness.get("priority") == "Medium"
    )


    gap_points = 15

    gap_points -= (
        high_priority_gaps * 3
    )

    gap_points -= (
        medium_priority_gaps * 1
    )

    gap_points = max(
        gap_points,
        0
    )


    # -------------------------
    # FINAL SCORE
    # -------------------------

    final_score = (

        profile_score
        + skill_score
        + github_activity_points
        + repository_score
        + gap_points

    )


    final_score = round(
        min(final_score, 100)
    )


    # -------------------------
    # READINESS LEVEL
    # -------------------------

    if final_score >= 85:

        readiness_level = (
            "Highly Ready Developer"
        )

    elif final_score >= 70:

        readiness_level = (
            "Strongly Progressing"
        )

    elif final_score >= 50:

        readiness_level = (
            "Developing Developer"
        )

    else:

        readiness_level = (
            "Early Stage Developer"
        )


    # -------------------------
    # READINESS MESSAGE
    # -------------------------

    if final_score >= 85:

        readiness_message = (
            "Your developer profile shows strong technical "
            "growth, activity, and project readiness."
        )

    elif final_score >= 70:

        readiness_message = (
            "You are making strong progress. Focus on "
            "improving your weaker areas to become more "
            "industry ready."
        )

    elif final_score >= 50:

        readiness_message = (
            "You have a developing foundation. Build more "
            "projects and strengthen your core technical skills."
        )

    else:

        readiness_message = (
            "You are at an early stage. Focus on building "
            "your profile, skills, projects, and GitHub activity."
        )

# -------------------------
# PRIORITY ACTION
# -------------------------

    priority_action = "Keep building your developer profile."

    if profile_score < 20:

        priority_action = (
            "Complete your developer profile by adding "
            "your missing information."
        )

    elif skill_score < 20:

        priority_action = (
            "Strengthen your technical skills and focus "
            "on your weaker technologies."
        )

    elif github_activity_points < 15:

        priority_action = (
            "Increase your GitHub activity by making "
            "regular contributions and improving your repositories."
        )

    elif repository_score < 20:

        priority_action = (
            "Build more production-level projects to "
            "demonstrate your development abilities."
        )

    elif gap_points < 15:

        priority_action = (
            "Work on the developer gaps identified by "
            "DevMind to improve your overall readiness."
        )

        # -------------------------
        # SCORE STATUS
        # -------------------------

    if final_score >= 80:

        score_status = "Excellent"

    elif final_score >= 65:

        score_status = "Improving"

    elif final_score >= 50:

        score_status = "Needs Attention"

    else:

        score_status = "Getting Started"


    return {

        "score": final_score,

        "level": readiness_level,

        "message": readiness_message,

        "priority_action": priority_action,

        "score_status": score_status,


        "profile_points": round(
            profile_score
        ),

        "skill_points": round(
            skill_score
        ),

        "activity_points": round(
            github_activity_points
        ),

        "project_points": round(
            repository_score
        ),

        "gap_points": round(
            gap_points
        )

    }