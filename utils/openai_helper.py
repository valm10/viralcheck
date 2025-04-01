import os
import logging
from openai import OpenAI, OpenAIError, RateLimitError
from dotenv import load_dotenv
from PIL.Image import Image
from utils.mock_predictor import get_mock_prediction

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    level=logging.INFO
)

# Get API key 
api_key = os.getenv("OPENAI_API_KEY")
GPT_AVAILABLE = api_key is not None
client = OpenAI(api_key=api_key) if GPT_AVAILABLE else None


def generate_prediction(title: str, image: Image) -> dict:

    if not client:
        logging.warning("No API key found. Falling back to mock prediction.")
        return get_mock_prediction(title)

    width, height = image.size
    prompt = f"""
You are a YouTube content strategist and viral video expert.

1. Rewrite this video title to make it more clickable and engaging.
2. Based on the thumbnail resolution ({width}x{height}), suggest one improvement.

Original Title: {title}

Respond using this exact format:
Suggestion: <Improved title>
Tip: <Copywriting tip>
Thumbnail: <Thumbnail improvement tip>
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt.strip()}]
        )

        content = response.choices[0].message.content.strip().split("\n")

        suggestion = _extract_value(content, "Suggestion:")
        tip = _extract_value(content, "Tip:")
        thumbnail_tip = _extract_value(content, "Thumbnail:")

        return {
            "suggested_title": suggestion,
            "tip": tip,
            "thumbnail_tip": thumbnail_tip,
            "score": 78,
            "top_videos": get_mock_prediction(title)["top_videos"]
        }

    except (OpenAIError, RateLimitError) as e:
        logging.error(f"OpenAI error: {e}")
        return get_mock_prediction(title)
    except Exception as e:
        logging.exception("Unexpected error in GPT prediction.")
        return get_mock_prediction(title)


def _extract_value(lines: list, prefix: str) -> str:

    for line in lines:
        if line.strip().startswith(prefix):
            return line.replace(prefix, "").strip()
    return "Not provided."
