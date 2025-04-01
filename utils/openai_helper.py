import os
import logging
from openai import OpenAI, OpenAIError
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

# Initialize GPT client
api_key = os.getenv("OPENAI_API_KEY")
GPT_AVAILABLE = api_key is not None
client = OpenAI(api_key=api_key) if GPT_AVAILABLE else None


def generate_prediction(title: str, image: Image) -> dict:
    """
    Uses GPT-4o to rewrite a YouTube video title and give thumbnail feedback.
    Falls back to mock data if API is not available or an error occurs.

    Args:
        title (str): YouTube video title
        image (Image): PIL image object

    Returns:
        dict: prediction results (suggested title, tips, etc.)
    """
    if not client:
        logging.warning("⚠️ OpenAI client unavailable — using mock data.")
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
            "score": 78,
            "top_videos": get_mock_prediction(title)["top_videos"]
        }

    except OpenAIError as e:
        logging.error(f"OpenAI error: {e}")
        return get_mock_prediction(title)
    except Exception as e:
        logging.exception("Unexpected error in GPT prediction.")
        return get_mock_prediction(title)


def _build_prompt(title: str, width: int, height: int) -> str:
    """
    Builds the GPT prompt dynamically.

    Args:
        title (str): Original title
        width (int): Thumbnail width
        height (int): Thumbnail height

    Returns:
        str: The full prompt string
    """
    return f"""
You are an expert in YouTube virality optimization.

Given the following video title and thumbnail size, improve the title and give suggestions.

Title: {title}
Thumbnail size: {width}x{height}

Reply in this format:
Suggestion: <better title>
Tip: <how to improve the title>
Thumbnail: <suggestion for the thumbnail>
""".strip()


def _extract(lines: list, key: str) -> str:
    """
    Extracts a value from a GPT response line.

    Args:
        lines (list): GPT response lines
        key (str): Prefix to match

    Returns:
        str: Extracted text, or fallback
    """
    for line in lines:
        if line.strip().lower().startswith(key.lower()):
            return line.split(":", 1)[-1].strip()
    return "No response provided."
