import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from PIL.Image import Image
from utils.youtube_scraper import search_youtube

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
GPT_AVAILABLE = api_key is not None
client = OpenAI(api_key=api_key) if GPT_AVAILABLE else None

def generate_prediction(title: str, image: Image) -> dict:
    width, height = image.size
    prompt = _build_prompt(title, width, height)

    try:
        if not client:
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

    except OpenAIError:
        return _fallback_prediction(title)

    except Exception:
        return _fallback_prediction(title)

def _build_prompt(title: str, width: int, height: int) -> str:
    return f"""
You're a YouTube content strategist.

Analyze this video title and thumbnail resolution:
- Title: {title}
- Thumbnail size: {width}x{height}

Reply with:
Suggestion: <better title>
Tip: <tip to improve title>
Thumbnail: <tip to improve thumbnail>
""".strip()

def _extract(lines: list, key: str) -> str:
    for line in lines:
        if line.strip().lower().startswith(key.lower()):
            return line.split(":", 1)[-1].strip()
    return "No response."

def _fallback_prediction(title: str) -> dict:
    return {
        "suggested_title": f"{title} – The Unexpected Twist!",
        "tip": "Use curiosity and emotion to boost clicks.",
        "thumbnail_tip": "Use a close-up face and bold text with contrast.",
        "top_videos": search_youtube(title)
    }
