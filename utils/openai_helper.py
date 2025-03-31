import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_title_suggestion(title: str) -> dict:
    """
    Uses GPT to improve a YouTube video title and provide a copywriting tip.

    Args:
        title (str): Original video title from user input.

    Returns:
        dict: {
            'suggested_title': str,
            'tip': str
        }
    """

    prompt = f"""
You are an expert in creating viral YouTube content.
Improve the following video title to make it more engaging and click-worthy:

Title: {title}

Then, provide one short copywriting tip to improve its click-through rate (CTR).
Respond in the following format:
Suggestion: <your new title>
Tip: <your copywriting tip>
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt.strip()}
        ]
    )

    content = response.choices[0].message.content.strip().split("\n")

    suggestion = content[0].replace("Suggestion:", "").strip() if len(content) > 0 else "No suggestion."
    tip = content[1].replace("Tip:", "").strip() if len(content) > 1 else "No tip."

    return {
        "suggested_title": suggestion,
        "tip": tip
    }
