import os
import logging
from openai import OpenAI, OpenAIError, APIConnectionError, AuthenticationError, RateLimitError
from dotenv import load_dotenv
from PIL import Image
from utils.mock_predictor import get_mock_prediction
from utils.youtube_scraper import search_youtube


#Load variables
load_dotenv()

#Configure logging
logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    level=logging.DEBUG  # Set to DEBUG for more granular logs
)

#Initialize GPT client
api_key = os.getenv("OPENAI_API_KEY")
GPT_AVAILABLE = api_key is not None
client = OpenAI(api_key=api_key) if GPT_AVAILABLE else None

def generate_prediction(title: str, image: Image) -> dict:
    """
    Generates a prediction using OpenAI's GPT model based on the provided title and image.
    Falls back to mock data if the OpenAI client is unavailable or an error occurs.
    """
    if not client:
        logging.warning("⚠️ OpenAI client unavailable — using mock data.")
        return get_mock_prediction(title)

    width, height = image.size
    prompt = _build_prompt(title, width, height)

    try:
        logging.debug(f"Sending prompt to OpenAI: {prompt}")
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
            "top_videos": search_youtube(title)
        }

    except APIConnectionError as e:
        logging.error(f"API connection error: {e}")
    except AuthenticationError as e:
        logging.error(f"Authentication error: {e}")
    except RateLimitError as e:
        logging.error(f"Rate limit error: {e}")
    except OpenAIError as e:
        logging.error(f"OpenAI error: {e}")
    except Exception as e:
        logging.exception("Unexpected error in GPT prediction.")
    
    return get_mock_prediction(title)

def _build_prompt(title: str, width: int, height: int) -> str:
    """
    Constructs a prompt for the OpenAI API based on the video title and thumbnail dimensions.
    """
    return f"""
You are an expert in YouTube virality optimization.

Given the following video title and thumbnail size, provide suggestions to enhance its appeal:

Title: {title}
Thumbnail size: {width}x{height}

Please provide:
- A more engaging title suggestion.
- A tip to improve the title.
- A suggestion for the thumbnail design.
""".strip()

def _extract(lines: list, key: str) -> str:
    """
    Extracts the content corresponding to a specific key from the response lines.
    """
    for line in lines:
        if line.strip().lower().startswith(key.lower()):
            return line.split(":", 1)[-1].strip()
    return f"No {key.lower()} found."
 
