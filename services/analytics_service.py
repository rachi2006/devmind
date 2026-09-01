def calculate_analytics(profile, repositories, languages):

    # -----------------------------
    # BASIC DATA
    # -----------------------------

    public_repos = profile.get(
        "public_repos", 0
    )

    followers = profile.get(
        "followers", 0
    )

    stars = 0

    for repo in repositories:
        stars += repo.get(
            "stargazers_count", 0
        )


    # -----------------------------
    # REPOSITORY SCORE
    # Maximum = 30
    # -----------------------------

    repository_score = min(
        30,
        public_repos * 3
    )


    # -----------------------------
    # TECHNOLOGY SCORE
    # Maximum = 25
    # -----------------------------

    technology_score = min(
        25,
        len(languages) * 4
    )


    # -----------------------------
    # COMMUNITY SCORE
    # Maximum = 15
    # -----------------------------

    community_score = min(
        15,
        followers * 0.5
    )


    # -----------------------------
    # PROJECT IMPACT SCORE
    # Maximum = 30
    # -----------------------------

    project_impact_score = min(
        30,
        stars * 2
    )


    # -----------------------------
    # OVERALL SCORE
    # Maximum = 100
    # -----------------------------

    productivity_score = round(

        repository_score
        + technology_score
        + community_score
        + project_impact_score

    )


    return {

        "public_repos": public_repos,

        "followers": followers,

        "stars": stars,

        "language_count": len(languages),

        "repository_score": round(
            repository_score
        ),

        "technology_score": round(
            technology_score
        ),

        "community_score": round(
            community_score
        ),

        "project_impact_score": round(
            project_impact_score
        ),

        "productivity_score": productivity_score

    }


