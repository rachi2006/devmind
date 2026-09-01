import os

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()


# Get NVIDIA API key
api_key = os.getenv("NVIDIA_API_KEY")


# Create NVIDIA client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)


def generate_ai_coach_response(question, github_data):

    # Developer profile data
    developer_context = f"""
Developer Profile Analysis:

GitHub Username:
{github_data.get("github_username", "Unknown")}

Productivity Score:
{github_data.get("productivity_score", 0)}/100

Activity Score:
{github_data.get("activity_score", 0)}/100

Public Repositories:
{github_data.get("public_repos", 0)}

Programming Languages:
{", ".join(github_data.get("languages", []))}

Recent Commits:
{github_data.get("recent_commits", 0)}

Active Days:
{github_data.get("active_days", 0)}

Development Consistency:
{github_data.get("consistency", "Unknown")}
"""


    # AI instructions
    system_prompt = """
You are DevMind AI Coach, an intelligent developer career and
GitHub profile analysis assistant.

Analyze the developer profile and answer the user's question.

IMPORTANT RESPONSE RULES:

1. Do NOT use Markdown tables.
2. Do NOT use table formatting.
3. Do NOT use pipe symbols.
4. Use simple headings.
5. Use bullet points starting with -.
6. Keep the response clean and professional.
7. Give clear strengths.
8. Give clear weaknesses when relevant.
9. Give practical recommendations.
10. Use simple readable text.
11. Base your response only on the developer data provided.

Use this structure when appropriate:

Strengths:
- Strength 1
- Strength 2
- Strength 3

Weaknesses:
- Weakness 1
- Weakness 2
- Weakness 3

Recommendations:
- Recommendation 1
- Recommendation 2
- Recommendation 3

Final Assessment:
Write a short personalized conclusion.
"""


    try:

        response = client.chat.completions.create(

            model="nvidia/nemotron-3-super-120b-a12b",

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": f"""
{developer_context}

User Question:
{question}
"""
                }

            ],

            temperature=0.7,

            max_tokens=700

        )


        return response.choices[0].message.content


    except Exception as error:

        print("\n========== AI COACH ERROR ==========")
        print(type(error).__name__)
        print(error)
        print("====================================\n")


        return (
            "DevMind AI Coach is temporarily unavailable. "
            "Please check the AI API configuration."
        )