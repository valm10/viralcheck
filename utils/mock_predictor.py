# Simulated prediction function
def get_mock_prediction(title):
    return {
        "score": 78,
        "suggested_title": f"🔥 {title} | You Won't Believe This!",
        "tip": "Use emotional or curiosity-driven hooks to boost clicks.",
        "thumbnail_tip": "Use bold text, contrasting colors, and close-up faces to catch attention.",
        "top_videos": [
            {"title": "Video A", "score": 92},
            {"title": "Video B", "score": 88},
            {"title": "Video C", "score": 84}
        ]
    }

