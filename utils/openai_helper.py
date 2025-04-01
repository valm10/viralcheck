import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from utils.mock_predictor import get_mock_prediction
from PIL import Image

# Load environment
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
GPT_AVAILABLE = api_key is not None

if GPT_AVAILABLE:
    client = OpenAI(api_key=api_key)


def generate_prediction(title: str, image: Image.Image) -> dict:
    """
    Uses GPT-4o to improve the YouTube title and give thumbnail tips.
    Falls back to mock prediction if OpenAI key is missing or fails.

    Args:
        title (str): Original YouTube video title
        image (PIL.Image.Image): Uploaded thumbnail image

    Returns:
        dict: {
            'suggested_title': str,
            'tip': str,
            'thumbnail_tip': str,
            'score': int,
            'top_videos': list[dict]
        }
    """

    # If no API key, fallback immediately
    if not GPT_AVAILABLE:
        print("⚠️ No API key found. Using mock data.")
        return get_mock_prediction(title)

    # Get thumbnail dimensions
    width, height = image.size

    # Create dynamic GPT prompt
    prompt = f"""
You are a YouTube content optimization expert.

1. Rewrite the following video title to make it more engaging and curiosity driven to improve click through rate (CTR).
2. Analyze the thumbnail resolution and give a professional improvement tip based on the dimensions ({width}x{height}).

Original Title: {title}

Respond in this format:
Suggestion: <your improved title>
Tip: <tip about the title>
ThumbnailTip: <tip about improving the thumbnail>
"""

    try:
        # Send request to GPT
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt.strip()}]
        )

        content = response.choices[0].message.content.strip().split("\n")

        # Parse each field from the GPT response
        suggestion = next((line.replace("Suggestion:", "").strip() for line in content if line.startswith("Suggestion:")), "No suggestion.")
        tip = next((line.replace("Tip:", "").strip() for line in content if line.startswith("Tip:")), "No tip.")
        thumbnail_tip = next((line.replace("ThumbnailTip:", "").strip() for line in content if line.startswith("ThumbnailTip:")), "No thumbnail tip.")

        return {
            "suggested_title": suggestion,
            "tip": tip,
            "thumbnail_tip": thumbnail_tip,
            "score": 78,  
            "top_videos": get_mock_prediction(title)["top_videos"]
        }

    except OpenAIError as e:
        print("⚠️ GPT error. Using fallback. Reason:", e)
        return get_mock_prediction(title)
