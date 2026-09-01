def detect_developer_weaknesses(
    skill_analysis,
    user_skills,
    github_languages,
    github_data
):

    weaknesses = []


    # Convert profile skills into a clean list

    if isinstance(user_skills, str):

        profile_skills = [

            skill.strip().lower()

            for skill in user_skills.split(",")

            if skill.strip()

        ]

    else:

        profile_skills = []


    # Check for GitHub languages not listed
    # in the developer profile

    for language in github_languages:

        if language.lower() not in profile_skills:

            weaknesses.append({

                "title":
                f"{language} is not listed in your profile",

                "description":
                (
                    f"{language} appears in your GitHub "
                    f"repositories, but it is not listed "
                    f"as one of your main skills."
                ),

                "priority": "Medium"

            })


    # Check weak or developing skills

    for item in skill_analysis:

        if item["level"] == "Learning":

            weaknesses.append({

                "title":
                f"Strengthen {item['skill']}",

                "description":
                (
                    f"Your current evidence for "
                    f"{item['skill']} is limited. "
                    f"Build more projects and practice "
                    f"the fundamentals."
                ),

                "priority": "High"

            })


    # Check repository activity

    public_repos = github_data.get(
        "public_repos",
        0
    )


    if public_repos < 3:

        weaknesses.append({

            "title":
            "Limited project portfolio",

            "description":
            (
                "Your GitHub profile has a limited number "
                "of public repositories. Build and publish "
                "more meaningful projects."
            ),

            "priority": "High"

        })


    # Check recent commits

    recent_commits = github_data.get(
        "recent_commits",
        0
    )


    if recent_commits < 5:

        weaknesses.append({

            "title":
            "Low recent development activity",

            "description":
            (
                "Your recent GitHub activity appears low. "
                "Try maintaining consistent coding and "
                "project activity."
            ),

            "priority": "High"

        })


    # Check skill diversity

    total_skills = len(skill_analysis)


    if total_skills < 3:

        weaknesses.append({

            "title":
            "Limited skill diversity",

            "description":
            (
                "Your profile currently shows only a small "
                "number of technical skills. Consider "
                "developing complementary technologies."
            ),

            "priority": "Medium"

        })


    # Remove duplicate weaknesses

    unique_weaknesses = []


    existing_titles = set()


    for weakness in weaknesses:

        if weakness["title"] not in existing_titles:

            unique_weaknesses.append(
                weakness
            )

            existing_titles.add(
                weakness["title"]
            )


    # Return maximum 5 weaknesses

    return unique_weaknesses[:5]