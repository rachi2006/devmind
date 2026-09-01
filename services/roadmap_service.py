def generate_growth_roadmap(github_data):

    score = github_data.get(
        "productivity_score", 0
    )

    activity_score = github_data.get(
        "activity_score", 0
    )

    active_days = github_data.get(
        "active_days", 0
    )

    public_repos = github_data.get(
        "public_repos", 0
    )

    language_count = github_data.get(
        "language_count", 0
    )

    languages = github_data.get(
        "languages", []
    )


    priorities = []


    # -----------------------------
    # PROJECT PORTFOLIO
    # -----------------------------

    if public_repos < 5:

        priorities.append({
            "title": "Build a Stronger Project Portfolio",

            "description":
            "Create 2-3 complete real-world projects "
            "instead of many small practice repositories."
        })


    # -----------------------------
    # GITHUB CONSISTENCY
    # -----------------------------

    if active_days < 8:

        priorities.append({
            "title": "Improve Development Consistency",

            "description":
            "Work consistently and push meaningful updates "
            "to GitHub every week."
        })


    # -----------------------------
    # TECHNOLOGY DEPTH
    # -----------------------------

    if language_count < 5:

        priorities.append({
            "title": "Strengthen Technology Depth",

            "description":
            "Master your current technologies while gradually "
            "adding complementary skills."
        })


    # -----------------------------
    # ADVANCED PROFILE
    # -----------------------------

    if score >= 60:

        priorities.append({
            "title": "Build Production-Level Projects",

            "description":
            "Focus on authentication, databases, APIs, deployment "
            "and scalable application architecture."
        })


    # -----------------------------
    # HIGH ACTIVITY
    # -----------------------------

    if activity_score >= 60:

        priorities.append({
            "title": "Increase Project Impact",

            "description":
            "Improve documentation and build projects that "
            "solve real-world problems."
        })


    # -----------------------------
    # DEFAULT PRIORITY
    # -----------------------------

    if not priorities:

        priorities.append({
            "title": "Strengthen Your Developer Profile",

            "description":
            "Continue building projects and improving "
            "your technical portfolio."
        })


    # -----------------------------
    # NEXT PROJECT
    # -----------------------------

    if "Python" in languages:

        next_project = (
            "Build an advanced full-stack application using "
            "Python, Flask or Django, MongoDB and REST APIs."
        )

    elif "JavaScript" in languages:

        next_project = (
            "Build a modern full-stack web application with "
            "a frontend framework and backend API."
        )

    else:

        next_project = (
            "Build a complete end-to-end project using "
            "your strongest programming technology."
        )


    # -----------------------------
    # NEXT SKILL
    # -----------------------------

    if language_count <= 2:

        next_skill = (
            "Learn databases and backend development."
        )

    elif activity_score < 40:

        next_skill = (
            "Practice Git, GitHub workflows and "
            "consistent project development."
        )

    else:

        next_skill = (
            "Learn system design, APIs and scalable "
            "software architecture."
        )


    return {

        "priorities": priorities[:3],

        "next_project": next_project,

        "next_skill": next_skill

    }