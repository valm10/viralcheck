# utils/openai_helper.py

import os
import logging
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from PIL import Image
from utils.mock_predictor import get_mock_prediction
from utils.youtube_scraper import search_youtube

#Load environment variables
load_dotenv()

#Setup logging
logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    level=logging.INFO
)

#Initialize OpenAI
api_key = os.getenv("OPENAI_API_KEY")
GPT_AVAILABLE = api_key is not None
client = OpenAI(api_key=api_key) if GPT_AVAILABLE else None

def generate_prediction(title: str, image: Image) -> dict:
    """
    Generate AI-based suggestions for a YouTube title and thumbnail.
    Falls back to mock data if OpenAI fails or API key is not available.
    """
    if not client:
        logging.warning("⚠️ OpenAI not available. Using mock prediction.")
        return get_mock_prediction(title)

    width, height = image.size
    prompt = _build_prompt(title, width, height)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip().split("\n")

        return {
            "suggested_title": _extract(content, "Suggestion"),
            "tip": _extract(content, "Tip"),
            "thumbnail_tip": _extract(content, "Thumbnail"),
            "score": 90,
            "top_videos": search_youtube(title)

        }

    except OpenAIError as e:
        logging.error(f"OpenAI error: {e}")
        return get_mock_prediction(title)

    except Exception as e:
        logging.exception("Unexpected error")
        return get_mock_prediction(title)

def _build_prompt(title: str, width: int, height: int) -> str:
    return f"""
You are a YouTube growth expert, focused on CPR.

Given this video title and its thumbnail dimensions, provide suggestions to improve CTR.

Title: {title}
Thumbnail size: {width}x{height}

Respond with:
Suggestion: <Better title>
Tip: <Advice for title>
Thumbnail: <Advice for thumbnail>
""".strip()

def _extract(lines: list, key: str) -> str:
    for line in lines:
        if line.lower().startswith(key.lower()):
            return line.split(":", 1)[-1].strip()
    return f"No {key.lower()} found."
