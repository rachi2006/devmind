from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt

import requests
from requests.exceptions import RequestException

from bson import ObjectId
from datetime import datetime

from config import Config
from database.mongodb import users_collection

from services.analytics_service import calculate_analytics
from services.insight_service import generate_developer_insight
from services.activity_service import analyze_activity
from services.roadmap_service import generate_growth_roadmap
from services.ai_coach_service import generate_ai_coach_response
from services.skill_service import analyze_skills
from services.recommendation_service import generate_learning_recommendations
from services.weakness_service import detect_developer_weaknesses
from services.readiness_service import calculate_readiness_score

# --------------------------------------------------
# APP SETUP
# --------------------------------------------------

app = Flask(__name__)

app.config.from_object(Config)

bcrypt = Bcrypt(app)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("home.html")


# --------------------------------------------------
# REGISTER
# --------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")


    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")


    email = email.lower().strip()


    existing_user = users_collection.find_one(
        {"email": email}
    )


    if existing_user:
        return "Email already registered"


    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")


    user = {
        "name": name,
        "email": email,
        "password": hashed_password
    }


    users_collection.insert_one(user)


    return redirect("/login")


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")


    email = request.form.get("email")
    password = request.form.get("password")


    email = email.lower().strip()


    user = users_collection.find_one(
        {"email": email}
    )


    if not user:
        return "Invalid email or password"


    password_correct = bcrypt.check_password_hash(
        user["password"],
        password
    )


    if not password_correct:
        return "Invalid email or password"


    # Create user session

    session["user_id"] = str(
        user["_id"]
    )

    session["user_name"] = user["name"]


    return redirect("/dashboard")


# --------------------------------------------------
# CONNECT GITHUB
# --------------------------------------------------

@app.route("/connect-github", methods=["POST"])
def connect_github():

    # Check login

    if "user_id" not in session:
        return redirect("/login")


    # Get GitHub username

    github_username = request.form.get(
        "github_username",
        ""
    ).strip()


    if not github_username:
        return "Please enter a GitHub username"


    # --------------------------------------------------
    # GITHUB API URLS
    # --------------------------------------------------

    profile_url = (
        f"https://api.github.com/users/"
        f"{github_username}"
    )


    repos_url = (
        f"https://api.github.com/users/"
        f"{github_username}/repos"
    )


    events_url = (
        f"https://api.github.com/users/"
        f"{github_username}/events/public"
    )


    # --------------------------------------------------
    # REQUEST HEADERS
    # --------------------------------------------------

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "DevMind-App"
    }


    # --------------------------------------------------
    # FETCH GITHUB DATA SAFELY
    # --------------------------------------------------

    try:

        # Get profile

        profile_response = requests.get(
            profile_url,
            headers=headers,
            timeout=15
        )


        # Get repositories

        repos_response = requests.get(
            repos_url,
            headers=headers,
            params={
                "per_page": 100,
                "sort": "updated"
            },
            timeout=15
        )


        # Get public events

        events_response = requests.get(
            events_url,
            headers=headers,
            timeout=15
        )


    except RequestException as error:

        print(
            "GitHub API Connection Error:",
            error
        )

        return (
            "Unable to connect to GitHub right now. "
            "Please check your internet connection and try again."
        )


    # --------------------------------------------------
    # CHECK PROFILE RESPONSE
    # --------------------------------------------------

    if profile_response.status_code == 404:

        return "GitHub user not found"


    if profile_response.status_code != 200:

        print(
            "GitHub Profile Error:",
            profile_response.status_code
        )

        return (
            "Unable to fetch GitHub profile. "
            "Please try again later."
        )


    # Convert profile response

    profile = profile_response.json()


    # --------------------------------------------------
    # GET REPOSITORIES
    # --------------------------------------------------

    repositories = []


    if repos_response.status_code == 200:

        repositories = repos_response.json()

    else:

        print(
            "GitHub Repository Error:",
            repos_response.status_code
        )


    # --------------------------------------------------
    # GET EVENTS
    # --------------------------------------------------

    events = []


    if events_response.status_code == 200:

        events = events_response.json()

    else:

        print(
            "GitHub Events Error:",
            events_response.status_code
        )


    # --------------------------------------------------
    # FIND PROGRAMMING LANGUAGES
    # --------------------------------------------------

    languages = set()


    for repo in repositories:

        if repo.get("language"):

            languages.add(
                repo["language"]
            )


    languages = list(
        languages
    )


    # --------------------------------------------------
    # ANALYTICS ENGINE
    # --------------------------------------------------

    analytics = calculate_analytics(
        profile,
        repositories,
        languages
    )


    # --------------------------------------------------
    # ACTIVITY ENGINE
    # --------------------------------------------------

    activity_data = analyze_activity(
        events
    )


    # --------------------------------------------------
    # GROWTH ROADMAP ENGINE
    # --------------------------------------------------

    roadmap = generate_growth_roadmap({

        "languages": languages,

        **analytics,

        **activity_data

    })


    # --------------------------------------------------
    # DEVELOPER INSIGHT ENGINE
    # --------------------------------------------------

    developer_insight = generate_developer_insight({

        "languages": languages,

        **analytics,

        **activity_data

    })


    # --------------------------------------------------
    # BUILD COMPLETE GITHUB DATA
    # --------------------------------------------------

    github_data = {

        "github_username": github_username,

        "github_name": profile.get(
            "name"
        ) or github_username,


        "avatar_url": profile.get(
            "avatar_url"
        ),


        "languages": languages,


        # Analytics data

        **analytics,


        # Activity data

        **activity_data,


        # AI developer analysis

        "developer_insight": developer_insight,


        # Growth roadmap

        "growth_roadmap": roadmap
    }


    # --------------------------------------------------
    # SAVE DATA TO MONGODB
    # --------------------------------------------------

    users_collection.update_one(

        {
            "_id": ObjectId(
                session["user_id"]
            )
        },

        {
            "$set": {
                "github": github_data
            }
        }

    )


    # --------------------------------------------------
    # REDIRECT TO DASHBOARD
    # --------------------------------------------------

    return redirect("/dashboard")

# AI DEVELOPER COACH

@app.route("/ai-coach", methods=["POST"])
def ai_coach():

    if "user_id" not in session:
        return redirect("/login")

    question = request.form.get("question", "").strip()

    if not question:
        return redirect("/dashboard")

    user = users_collection.find_one(
        {
            "_id": ObjectId(session["user_id"])
        }
    )

    github_data = user.get("github")

    if not github_data:
        return redirect("/dashboard")

    answer = generate_ai_coach_response(
        question,
        github_data
    )

    conversation = {
    "question": question,
    "answer": answer,
    "created_at": datetime.utcnow().strftime(
        "%d %b %Y, %I:%M %p"
    )
}
    users_collection.update_one(
    {
        "_id": ObjectId(session["user_id"])
    },
    {
        "$push": {
            "github.ai_coach_history": conversation
        }
    }
)

    return redirect("/dashboard")

# CLEAR AI COACH HISTORY
@app.route("/clear-ai-history", methods=["POST"])
def clear_ai_history():

    if "user_id" not in session:
        return redirect("/login")


    users_collection.update_one(

        {
            "_id": ObjectId(session["user_id"])
        },

        {
            "$set": {
                "github.ai_coach_history": []
            }
        }

    )


    return redirect("/dashboard")


@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect("/login")


    user = users_collection.find_one(
        {
            "_id": ObjectId(session["user_id"])
        }
    )


    if request.method == "POST":

        bio = request.form.get("bio", "").strip()

        career_goal = request.form.get(
            "career_goal", ""
        ).strip()

        skills = request.form.get(
            "skills", ""
        ).strip()


        users_collection.update_one(

            {
                "_id": ObjectId(session["user_id"])
            },

            {
                "$set": {

                    "developer_profile": {

                        "bio": bio,

                        "career_goal": career_goal,

                        "skills": skills

                    }

                }

            }

        )


        return redirect("/profile")


    return render_template(

        "edit_profile.html",

        user=user

    )



# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")


    user = users_collection.find_one(

        {
            "_id": ObjectId(
                session["user_id"]
            )
        }

    )


    github_data = user.get(
        "github"
    )


    return render_template(

        "dashboard.html",

        user_name=session["user_name"],

        github_data=github_data,

        user=user


    )


@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")


    user = users_collection.find_one(
        {
            "_id": ObjectId(session["user_id"])
        }
    )


    # Get developer profile safely
    developer_profile = user.get(
        "developer_profile",
        {}
    )


    # Calculate profile completion
    completed_fields = 0
    total_fields = 6


    if user.get("name"):
        completed_fields += 1


    if user.get("email"):
        completed_fields += 1


    if developer_profile.get("bio"):
        completed_fields += 1


    if developer_profile.get("career_goal"):
        completed_fields += 1


    if developer_profile.get("skills"):
        completed_fields += 1


    if user.get("github"):
        completed_fields += 1


    completion_percentage = int(
        (completed_fields / total_fields) * 100
    )
    
    if completion_percentage < 40:

        profile_strength = "Beginner Profile"


    elif completion_percentage < 70:

        profile_strength = "Growing Profile"


    elif completion_percentage < 100:

        profile_strength = "Strong Developer Profile"


    else:

        profile_strength = "Excellent Developer Profile"

    # Get profile skills

    user_skills = developer_profile.get(
        "skills",
        ""
    )


    # Get GitHub languages safely

    github_data = user.get(
        "github",
        {}
    )


    github_languages = github_data.get(
        "languages",
        []
    )


    # Analyze developer skills

    skill_analysis = analyze_skills(
        user_skills,
        github_languages
    )

    # Generate personalized learning recommendations

    learning_recommendations = (
        generate_learning_recommendations(
            skill_analysis
        )
    )

    # Detect developer weaknesses

    developer_weaknesses = (
        detect_developer_weaknesses(
            skill_analysis,
            user_skills,
            github_languages,
            github_data
        )
    )

    # Calculate developer readiness

    readiness_data = calculate_readiness_score(
        completion_percentage,
        skill_analysis,
        github_data,
        developer_weaknesses
    )


    return render_template(
        "profile.html",
        user=user,
        completion_percentage=completion_percentage,
        profile_strength=profile_strength,
        skill_analysis=skill_analysis,
        learning_recommendations=learning_recommendations,
        developer_weaknesses=developer_weaknesses,
        readiness_data=readiness_data
    )


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )