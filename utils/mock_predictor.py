# Simulated prediction function
def get_mock_prediction(title):
    return {
        "score": 78, #Fake Score
        "suggested_title": f"🔥 {title} | You Won't Believe This!",
        "tip": "Use emotional or curiosity-driven hooks to boost clicks.",
        "top_videos": [
            {"title": "How I Got 1M Views in 1 Week", "score": 92},
            {"title": "This Changed My Life Forever", "score": 88},
            {"title": "Secrets You Were Never Told", "score": 84},
        ]
    }
