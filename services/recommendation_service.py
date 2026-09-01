def generate_learning_recommendations(skill_analysis):

    recommendations = []


    for item in skill_analysis:

        skill = item["skill"]

        score = item["score"]

        level = item["level"]


        # Skills that need improvement

        if level == "Learning":

            recommendations.append({

                "title": f"Strengthen {skill}",

                "description": (
                    f"Your current analysis shows that "
                    f"{skill} is still developing. "
                    f"Practice it with small projects and "
                    f"focus on the fundamentals."
                ),

                "priority": "High"

            })


        # Intermediate skills

        elif level == "Intermediate":

            recommendations.append({

                "title": f"Improve {skill}",

                "description": (
                    f"You already have a foundation in "
                    f"{skill}. Focus on advanced concepts "
                    f"and build practical projects."
                ),

                "priority": "Medium"

            })


        # Strong skills

        elif level == "Strong":

            recommendations.append({

                "title": f"Advance your {skill} skills",

                "description": (
                    f"{skill} is one of your strongest "
                    f"skills. Continue improving by building "
                    f"larger and more challenging projects."
                ),

                "priority": "Low"

            })


    # Sort recommendations by priority

    priority_order = {

        "High": 1,

        "Medium": 2,

        "Low": 3

    }


    recommendations.sort(

        key=lambda item:
        priority_order[item["priority"]]

    )


    # Return only the top 5 recommendations

    return recommendations[:5]