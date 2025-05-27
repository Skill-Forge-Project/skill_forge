import os
from openai import OpenAI
from sqlalchemy import text
from extensions import db
from dotenv import load_dotenv

load_dotenv()


OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
client = OpenAI(
    api_key=OPEN_AI_KEY,
)


# Generate new Underworld challenge for the specific boss
def generate_underworld_challenge(boss_id):
    """
    Generate a new Underworld challenge for the specified boss.
    
    Args:
        boss_name (str): Name of the boss.
        boss_title (str): Title of the boss.
        boss_language (str): Language of the boss.
        boss_difficulty (str): Difficulty level of the boss.
        boss_specialty (str): Specialty of the boss.
    
    Returns:
        str: Generated Underworld challenge description.
    """

    # Get boss details from the database
    query = text("SELECT * FROM bosses WHERE id = :boss_id")
    result = db.session.execute(query, {"boss_id": boss_id})
    boss = result.fetchone()
    if not boss:
        return "Boss not found."

    boss_name = boss.boss_name
    boss_title = boss.boss_title
    boss_language = boss.boss_language
    boss_difficulty = boss.boss_difficulty
    boss_specialty = boss.boss_specialty
    boss_description = boss.boss_description

    prompt = (
        f"Generate an Underworld challenge for the following boss:\n"
        f"Your Name is {boss_name}\n"
        f"your title is {boss_title}\n"
        f"your language is {boss_language}\n"
        f"your difficulty is {boss_difficulty}\n"
        f"your specialty is {boss_specialty}\n"
        f"your description is {boss_description}\n"
        
        f"Generate a unique and engaging coding challenge that fits the above criteria - language, difficulty and specialty.\n"
        f"Make the challenge suitable for a coding competition, ensuring it is challenging yet solvable.\n"
        f"Write the challenge following your flair - name, title and description.\n"
        f"DO NOT generate and add any code snippets to the challenge.\n"
        f"Generated challenge should contain only the actual problem statement, without any additional explanations or instructions.\n"
        f"Make the challenge short and concise, focusing on the core problem to be solved.\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=False,
        messages=[
            {
                "role": "system",
                "content": "You are an AI boss that generates challenges for users.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content if response else "Failed to generate challenge."


