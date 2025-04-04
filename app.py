import streamlit as st
from PIL import Image
from utils.image_utils import check_aspect_ratio
from utils.mock_predictor import get_mock_prediction
from utils.openai_helper import generate_prediction

# --- Page Configuration ---
st.set_page_config(
    page_title="ViralCheck - YouTube Analyzer",
    page_icon="📈",
    layout="centered"
)

# --- App Title ---
st.title("🚀 ViralCheck")
st.caption("Boost your YouTube video’s performance with AI-powered title and thumbnail suggestions.")

st.divider()

# --- User Input Section ---
st.header("🎬 Video Details")

title_input = st.text_input("📌 Enter your YouTube video title")

thumbnail_file = st.file_uploader(
    "🖼️ Upload your video thumbnail (JPG or PNG)",
    type=["jpg", "jpeg", "png"]
)

image = None
is_valid = False

if thumbnail_file:
    image = Image.open(thumbnail_file)
    is_valid, width, height = check_aspect_ratio(image)

    st.image(image, caption=f"Thumbnail Preview ({width}x
