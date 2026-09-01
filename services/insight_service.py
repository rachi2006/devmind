def generate_developer_insight(github_data):

    insights = []

    score = github_data.get(
        "productivity_score", 0
    )

    public_repos = github_data.get(
        "public_repos", 0
    )

    languages = github_data.get(
        "languages", []
    )

    followers = github_data.get(
        "followers", 0
    )

    stars = github_data.get(
        "stars", 0
    )


    # Overall developer level

    if score >= 80:
        level = "Advanced Developer"

    elif score >= 60:
        level = "Growing Developer"

    elif score >= 40:
        level = "Developing Developer"

    else:
        level = "Early Stage Developer"


    # Repository analysis

    if public_repos >= 10:
        insights.append(
            "You have a strong portfolio of public projects."
        )

    elif public_repos >= 5:
        insights.append(
            "You are building a growing project portfolio."
        )

    else:
        insights.append(
            "Build more quality projects to strengthen your portfolio."
        )


    # Technology analysis

    if len(languages) >= 5:
        insights.append(
            "You have strong technology diversity."
        )

    elif len(languages) >= 3:
        insights.append(
            "You are developing skills across multiple technologies."
        )

    else:
        insights.append(
            "Explore more technologies to broaden your developer profile."
        )


    # Project impact

    if stars >= 10:
        insights.append(
            "Your projects are receiving strong community interest."
        )

    else:
        insights.append(
            "Focus on documentation and useful projects to increase project visibility."
        )


    # Community

    if followers >= 20:
        insights.append(
            "You have a growing developer network."
        )

    else:
        insights.append(
            "Share your projects and contribute to communities to grow your network."
        )


    # Recommended action

    if score < 40:
        recommendation = (
            "Focus on building 2-3 strong end-to-end projects "
            "and publishing them with clear README files."
        )

    elif score < 70:
        recommendation = (
            "Strengthen your portfolio with advanced projects "
            "and improve consistency in your GitHub activity."
        )

    else:
        recommendation = (
            "Focus on project quality, open-source contributions, "
            "and demonstrating real-world impact."
        )


    return {

        "developer_level": level,

        "insights": insights,

        "recommendation": recommendation

    }