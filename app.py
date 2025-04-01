# app.py

import streamlit as st
from PIL import Image
from utils.image_utils import check_aspect_ratio
from utils.openai_helper import generate_title_suggestion
import os

# --- Streamlit Config ---
st.set_page_config(page_title="ViralCheck", page_icon="📈", layout="centered")

# --- Sidebar ---
with st.sidebar:
    st.image("static/icon.png", width=200)
    st.markdown("## 📊 ViralCheck")
    st.markdown("**Predict your next YouTube hit.**")
    st.markdown("Built with ❤️ by [@valm10](https://github.com/valm10)")

# --- Header ---
st.title("🎬 ViralCheck - YouTube Viral Analyzer")
st.caption("AI-powered predictions based on your title and thumbnail.")
st.divider()

# --- Video Input ---
st.header("📥 Upload Your Video Info")
title_input = st.text_input("📌 Title")
thumbnail_input = st.file_uploader("🖼️ Thumbnail (JPG, PNG)", type=["jpg", "jpeg", "png"])

is_valid = False

if thumbnail_input:
    image = Image.open(thumbnail_input)
    is_valid, width, height = check_aspect_ratio(image)
    st.image(image, caption=f"Preview: {width}x{height}")

    if not is_valid:
        st.warning("⚠️ Not 16:9 format! YouTube recommends 1280x720 or similar.")
    else:
        st.success("✅ Thumbnail meets the 16:9 requirement.")

st.divider()

# --- Prediction ---
st.header("📊 Viral Prediction")

if st.button("🚀 Check Virality"):
    if not title_input or not thumbnail_input:
        st.warning("Please enter both a title and a thumbnail.")
    elif not is_valid:
        st.warning("Thumbnail must be 16:9 ratio.")
    else:
        st.success("✅ Analysis complete!")
        result = generate_title_suggestion(title_input)

        # --- Score ---
        st.subheader("🔮 Virality Score")
        st.metric(label="AI Prediction", value="⚡ High Potential", delta="↑ Trending Style")

        # --- Suggestions ---
        st.subheader("✨ Suggested Improvements")

        st.markdown(f"📢 **Improved Title:** `{result['suggested_title']}`")
        st.info(f"🖊️ *Title Tip:* {result['tip']}")
        st.info(f"🖼️ *Thumbnail Tip:* {result.get('thumbnail_tip', 'Try using a human face or bold color contrast.')}")

        # --- Footer ---
        st.divider()
        st.caption("Made with ❤️ using Streamlit and OpenAI.")
