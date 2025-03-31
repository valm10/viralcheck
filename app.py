# <-- Main Streamlit App -->

# Import Streamlit
import streamlit as st

# Import Pillow to handle image files
from PIL import Image

# Utility functions to check image size and make predictions
from utils.image_utils import check_aspect_ratio
from utils.openai_helper import generate_title_suggestion  # ✅ Import GPT logic

# <-- App Configuration -->

# Set up the Streamlit app
st.set_page_config(
    page_title="ViralCheck - Youtube Viral Analyzer",
    page_icon="📈",
    layout="centered"
)

st.title("Viral Check - YouTube Viral Analyser")
st.caption("Predict Your Next Viral Video in Seconds")
st.divider()

# <-- Input Section -->
st.header("🎬 Video Details")

# User input
title_input = st.text_input("📌 Your YouTube Video Title:")
thumbnail_input = st.file_uploader(
    "🖼️ Your YouTube Thumbnail (JPG, PNG):",
    type=["jpg", "jpeg", "png"]
)

is_valid = False  # Default if no image

# Image Upload Validation
if thumbnail_input is not None:
    image = Image.open(thumbnail_input)
    is_valid, width, height = check_aspect_ratio(image)

    st.image(image, caption=f"Thumbnail Preview ({width}x{height})")
    
    if not is_valid:
        st.warning("⚠️ This image is not in the recommended 16:9 YouTube thumbnail format (e.g. 1280x720).")
    else:
        st.success("✅ Thumbnail meets the 16:9 ratio requirement.")

# <-- Analysis Section -->
st.divider()
st.header("📊 Viral Prediction")

# User clicks button
if st.button("🚀 Check Virality"):
    if not title_input or not thumbnail_input:
        st.warning("⚠️ Please provide both a title and thumbnail.")
    elif not is_valid:
        st.warning("⚠️ Please upload a valid 16:9 thumbnail before analyzing.")
    else:
        # Get real AI suggestion
        result = generate_title_suggestion(title_input)

        st.success("✅ Analysis complete!")
        st.metric("Virality Score", "🔮 AI Prediction", delta="⚡ High Potential")

        st.image(thumbnail_input, caption="Your Thumbnail", use_column_width=True)

        st.subheader("🔁 Suggested Improvements")
        st.write(f"**Title Suggestion:** `{result['suggested_title']}`")
        st.info(result['tip'])

# Footer
st.divider()
st.caption("Made with ❤️ by [@valm10](https://github.com/valm10) · Powered by OpenAI + Streamlit")
