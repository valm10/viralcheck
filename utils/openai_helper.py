import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def generate_title_suggestion(title: str) -> dict:
    if not client:
        return {
            "suggested_title": f"🔥 {title} | You Won't Believe This!",
            "tip": "Use emotional or curiosity-driven hooks to boost clicks.",
            "thumbnail_tip": "Add a human face with strong emotion in the center of the thumbnail."
        }

    prompt = f"""
You are an expert in YouTube content strategy.
Improve the title below to maximize virality. Then give one title tip and one thumbnail tip.

Title: {title}

Format:
Suggestion: <better title>
Tip: <title improvement tip>
Thumbnail: <thumbnail improvement tip>
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt.strip()}]
    )

    content = response.choices[0].message.content.strip().split("\n")
    return {
        "suggested_title": content[0].replace("Suggestion:", "").strip(),
        "tip": content[1].replace("Tip:", "").strip(),
        "thumbnail_tip": content[2].replace("Thumbnail:", "").strip(),
    }
