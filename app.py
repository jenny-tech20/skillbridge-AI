from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# -----------------------------
# LOAD CSV
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "skills.csv")

skills_data = pd.read_csv(CSV_PATH)

# Clean column names
skills_data.columns = skills_data.columns.str.strip()

# Clean values
for column in skills_data.columns:
    skills_data[column] = skills_data[column].astype(str).str.strip()


# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# PROFILE PAGE
# -----------------------------
@app.route("/profile")
def profile():

    # Get roles from CSV
    roles = sorted(
        skills_data["role"]
        .dropna()
        .unique()
        .tolist()
    )

    return render_template(
        "profile.html",
        roles=roles
    )


# -----------------------------
# ANALYZE SKILLS
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    name = request.form.get("name", "").strip()
    degree = request.form.get("degree", "").strip()
    skills_input = request.form.get("skills", "").strip()
    target_role = request.form.get("target_role", "").strip()
    experience = request.form.get("experience", "").strip()

    # Convert user skills into list
    user_skills = [
        skill.strip().lower()
        for skill in skills_input.split(",")
        if skill.strip()
    ]

    # Find required skills for selected role
    role_data = skills_data[
        skills_data["role"].str.lower() == target_role.lower()
    ]

    required_skills = []

    if not role_data.empty:
        required_skills = (
            role_data["skill"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
            .unique()
            .tolist()
        )

    # -----------------------------
    # MATCH SKILLS
    # -----------------------------
    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in user_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # -----------------------------
    # READINESS SCORE
    # -----------------------------
    if len(required_skills) > 0:
        readiness_score = round(
            (len(matched_skills) / len(required_skills)) * 100
        )
    else:
        readiness_score = 0

    # -----------------------------
    # CAREER RECOMMENDATIONS
    # -----------------------------
    career_recommendations = []

    all_roles = skills_data["role"].dropna().unique()

    for role in all_roles:

        role_rows = skills_data[
            skills_data["role"].str.lower() == role.lower()
        ]

        role_skills = (
            role_rows["skill"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
            .unique()
            .tolist()
        )

        if len(role_skills) == 0:
            continue

        matches = len(
            set(user_skills).intersection(set(role_skills))
        )

        match_percentage = round(
            (matches / len(role_skills)) * 100
        )

        career_recommendations.append({
            "role": role,
            "match": match_percentage
        })

    # Sort by match percentage
    career_recommendations.sort(
        key=lambda x: x["match"],
        reverse=True
    )

    # Show top 3
    career_recommendations = career_recommendations[:3]

    # -----------------------------
    # DISPLAY SKILLS
    # -----------------------------
    matched_display = [
        skill.title()
        for skill in matched_skills
    ]

    missing_display = [
        skill.title()
        for skill in missing_skills
    ]

    # -----------------------------
    # SEND DATA TO ANALYSIS PAGE
    # -----------------------------
    return render_template(
        "analysis.html",

        name=name,
        degree=degree,
        experience=experience,
        target_role=target_role,

        readiness_score=readiness_score,

        matched_skills=matched_display,
        missing_skills=missing_display,

        career_recommendations=career_recommendations
    )


# -----------------------------
# ROADMAP
# -----------------------------
@app.route("/roadmap")
def roadmap():

    skills = request.args.get("skills", "")

    missing_skills = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]

    skill_plans = {

        "Python": {
            "days": 7,
            "plan": [
                "Python basics and syntax",
                "Variables, data types and operators",
                "Conditions and loops",
                "Functions and modules",
                "Lists, tuples, sets and dictionaries",
                "File handling and exception handling",
                "Mini project using Python"
            ]
        },

        "Sql": {
            "days": 7,
            "plan": [
                "SQL basics and database concepts",
                "SELECT, WHERE and ORDER BY",
                "GROUP BY and aggregate functions",
                "JOINs",
                "Subqueries",
                "INSERT, UPDATE and DELETE",
                "Practice queries and mini project"
            ]
        },

        "Pandas": {
            "days": 5,
            "plan": [
                "Pandas Series",
                "DataFrame creation and selection",
                "Filtering and sorting data",
                "Missing data and data cleaning",
                "Mini data analysis project"
            ]
        },

        "Numpy": {
            "days": 5,
            "plan": [
                "NumPy arrays",
                "Array indexing and slicing",
                "Array operations",
                "Mathematical functions",
                "Mini project using NumPy"
            ]
        },

        "Git": {
            "days": 4,
            "plan": [
                "Git and GitHub basics",
                "Repositories, commit and status",
                "Branches and merging",
                "Push project to GitHub"
            ]
        },

        "Machine Learning": {
            "days": 10,
            "plan": [
                "ML basics and types",
                "Dataset and features",
                "Data preprocessing",
                "Train-test split",
                "Linear Regression",
                "Classification basics",
                "Decision Trees",
                "Model evaluation",
                "Feature improvement",
                "Mini ML project"
            ]
        },

        "Java": {
            "days": 10,
            "plan": [
                "Java syntax and variables",
                "Conditions and loops",
                "Arrays and strings",
                "Methods",
                "Classes and objects",
                "Inheritance",
                "Polymorphism",
                "Exception handling",
                "Collections",
                "Mini project"
            ]
        },

        "Dsa": {
            "days": 14,
            "plan": [
                "Time and space complexity",
                "Arrays",
                "Strings",
                "Searching",
                "Sorting",
                "Linked Lists",
                "Stacks",
                "Queues",
                "Recursion",
                "Trees",
                "Binary Search Trees",
                "Graphs",
                "Greedy algorithms",
                "Dynamic Programming basics"
            ]
        },

        "Html": {
            "days": 3,
            "plan": [
                "HTML structure",
                "Forms, tables and links",
                "Build a simple webpage"
            ]
        },

        "Css": {
            "days": 4,
            "plan": [
                "CSS basics",
                "Selectors and box model",
                "Flexbox and Grid",
                "Responsive webpage"
            ]
        },

        "Javascript": {
            "days": 7,
            "plan": [
                "JavaScript basics",
                "Variables and data types",
                "Conditions and loops",
                "Functions",
                "Arrays and objects",
                "DOM manipulation",
                "Mini project"
            ]
        }
    }


    roadmap = []

    for skill in missing_skills:

        # Match skill names safely
        matched_key = None

        for key in skill_plans:

            if key.lower() == skill.lower():
                matched_key = key
                break

        if matched_key:

            roadmap.append({
                "skill": skill,
                "days": skill_plans[matched_key]["days"],
                "plan": skill_plans[matched_key]["plan"]
            })

        else:

            # Default plan for unknown skills
            roadmap.append({
                "skill": skill,
                "days": 5,
                "plan": [
                    f"Understand {skill} fundamentals",
                    f"Learn important concepts of {skill}",
                    f"Practice basic {skill} problems",
                    f"Build a small {skill} exercise",
                    f"Complete a mini project using {skill}"
                ]
            })


    return render_template(
        "roadmap.html",
        roadmap=roadmap
    )
if __name__ == "__main__":
    app.run(debug=True)