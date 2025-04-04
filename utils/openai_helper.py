import os
from dotenv import load_dotenv 
from openai import OpenAI, OpenAIError
from PIL.Image import Image
from utils.mock_predictor import get_mock_prediction


#Load enviroment variables from .env
load_dotenv

#Setep OpenAI client securely
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def generate_prediction(title: str, image: Image) -> dict:
    """
    Sends the title and thumbnail size to OpenAI to get a better title and tips.
    Falls back to mock if key is missing or error occurs.
    """
    if not client:
        return get_mock_prediction(title)

    width, height = image.size
    prompt = build_prompt(title, width, height)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip().split("\n")

        return {
            "suggested_title": extract_field(content, "Suggestion"),
            "tip": extract_field(content, "Tip"),
            "thumbnail_tip": extract_field(content, "Thumbnail"),
            "score": 88,
            "top_videos": get_mock_prediction(title)["top_videos"]
        }

    except (OpenAIError, Exception):
        return get_mock_prediction(title)

def build_prompt(title: str, width: int, height: int) -> str:
    return f"""
You are an expert in viral YouTube content creation, trying to boost the ctr as maximum as possible.

Given this video title and thumbnail size, improve the title and give helpful tips.

Title: {title}
Thumbnail: {width}x{height}

Reply in this exact format:
Suggestion: <better title>
Tip: <title improvement tip>
Thumbnail: <thumbnail improvement tip>
""".strip()

def extract_field(lines: list, key: str) -> str:
    for line in lines:
        if line.lower().startswith(key.lower()):
            return line.split(":", 1)[-1].strip()
    return f"No {key.lower()} provided."