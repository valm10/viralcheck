import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from utils.mock_predictor import get_mock_prediction

load_dotenv()

# Get the API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")

# Check if API key exists
GPT_AVAILABLE = api_key is not None

# Initialize OpenAI client only if the key is available
if GPT_AVAILABLE:
    client = OpenAI(api_key=api_key)


def generate_title_suggestion(title: str) -> dict:
    """
    Uses GPT to improve a YouTube video title and provide a copywriting tip.
    Falls back to a mock suggestion if OpenAI is not available or fails.

    Args:
        title (str): The original video title.

    Returns:
        dict: {
            'suggested_title': str,
            'tip': str,
            'score': int,
            'top_videos': list[dict]
        }
    """
    # Fallback if no API key
    if not GPT_AVAILABLE:
        print("⚠️ No API key detected. Using mock prediction.")
        return get_mock_prediction(title)

    # GPT prompt
    prompt = f"""
    You are an expert in creating viral YouTube content.
    Improve the following video title to make it more engaging and click-worthy:

    Title: {title}

    Then, provide one short copywriting tip to improve its click-through rate (CTR).

    Respond in this format:
    Suggestion: <your new title>
    Tip: <your copywriting tip>
    """

    try:
        # GPT API call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt.strip()}
            ]
        )

        content = response.choices[0].message.content.strip().split("\n")
        suggestion = content[0].replace("Suggestion:", "").strip() if len(content) > 0 else "No suggestion."
        tip = content[1].replace("Tip:", "").strip() if len(content) > 1 else "No tip."

        # Fallback top videos and mock score
        return {
            "suggested_title": suggestion,
            "tip": tip,
            "score": 78,  # placeholder score
            "top_videos": get_mock_prediction(title)['top_videos']
        }

    except OpenAIError as e:
        print("⚠️ OpenAI Error: Using mock fallback —", e)
        return get_mock_prediction(title)
