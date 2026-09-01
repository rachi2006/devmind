def analyze_skills(user_skills, github_languages):

    skill_analysis = []


    # Convert profile skills into a clean list

    if isinstance(user_skills, str):

        profile_skills = [

            skill.strip()

            for skill in user_skills.split(",")

            if skill.strip()

        ]

    else:

        profile_skills = []


    # Combine profile skills and GitHub languages

    all_skills = set(

        profile_skills +

        github_languages

    )


    for skill in all_skills:

        score = 40


        # If the skill is found in the profile

        if skill.lower() in [

            item.lower()

            for item in profile_skills

        ]:

            score += 30


        # If the skill is found in GitHub activity

        if skill.lower() in [

            item.lower()

            for item in github_languages

        ]:

            score += 30


        # Decide skill level

        if score >= 90:

            level = "Strong"


        elif score >= 70:

            level = "Intermediate"


        else:

            level = "Learning"


        skill_analysis.append({

            "skill": skill,

            "score": score,

            "level": level

        })


    # Sort strongest skills first

    skill_analysis.sort(

        key=lambda item: item["score"],

        reverse=True

    )


    return skill_analysis