import os
import logging
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from PIL.Image import Image
from utils.youtube_scraper import search_youtube

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    level=logging.INFO
)

api_key = os.getenv("OPENAI_API_KEY")
GPT_AVAILABLE = api_key is not None
client = OpenAI(api_key=api_key) if GPT_AVAILABLE else None

def generate_prediction(title: str, image: Image) -> dict:
    width, height = image.size
    prompt = _build_prompt(title, width, height)

    try:
        if not client:
            logging.warning("⚠️ GPT client not available. Returning fallback.")
            return _fallback_prediction(title)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content.strip().split("\n")
        return {
            "suggested_title": _extract(content, "Suggestion"),
            "tip": _extract(content, "Tip"),
            "thumbnail_tip": _extract(content, "Thumbnail"),
            "top_videos": search_youtube(title)
        }

    except OpenAIError as e:
        logging.error(f"OpenAI error: {e}")
        return _fallback_prediction(title)
    except Exception as e:
        logging.exception("Unexpected error in prediction.")
        return _fallback_prediction(title)

def _build_prompt(title: str, width: int, height: int) -> str:
    return f"""
You're a YouTube content optimization expert.

Given the title: {title}
And thumbnail size: {width}x{height}

Improve the title and give tips:

Suggestion: <improved title>
Tip: <title improvement tip>
Thumbnail: <thumbnail tip>
""".strip()

def _extract(lines: list, key: str) -> str:
    for line in lines:
        if line.strip().lower().startswith(key.lower()):
            return line.split(":", 1)[-1].strip()
    return "No data."

def _fallback_prediction(title: str) -> dict:
    return {
        "suggested_title": f"{title} – The Unexpected Twist!",
        "tip": "Use urgency or curiosity in your title for better clicks.",
        "thumbnail_tip": "Use big text and emotion-driven faces.",
        "top_videos": search_youtube(title)
    }
