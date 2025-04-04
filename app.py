import streamlit as st
from PIL import Image, UnidentifiedImageError
from utils.image_utils import check_aspect_ratio
from utils.openai_helper import generate_prediction

# --- Page Configuration ---
st.set_page_config(
    page_title="ViralCheck - YouTube Analyzer",
    page_icon="📈",
    layout="centered"
)

# --- Title ---
st.title("🚀 ViralCheck")
st.caption("Boost your YouTube video's performance with AI-powered title and thumbnail suggestions.")
st.divider()

# --- User Inputs ---
st.header("🎬 Video Details")
title_input = st.text_input("📌 Enter your YouTube video title")
thumbnail_file = st.file_uploader("🖼️ Upload your video thumbnail (JPG or PNG)", type=["jpg", "jpeg", "png"])

image = None
is_valid = False

# --- Thumbnail Validation ---
if thumbnail_file:
    try:
        image = Image.open(thumbnail_file)
        is_valid, width, height = check_aspect_ratio(image)

        st.image(image, caption=f"Thumbnail Preview ({width}x{height})", use_container_width=True)
        if is_valid:
            st.success("✅ Thumbnail is in 16:9 format.")
        else:
            st.warning("⚠️ Thumbnail is NOT in 16:9 format (recommended: 1280x720).")
    except UnidentifiedImageError:
        st.error("❌ Invalid image file. Please upload a valid JPG or PNG.")
        image = None

st.divider()
st.header("📊 Viral Prediction")

# --- Run Prediction ---
if st.button("🔍 Analyze with AI"):
    if not title_input:
        st.warning("⚠️ Please provide a video title.")
    elif not thumbnail_file or not image:
        st.warning("⚠️ Please upload a valid thumbnail image.")
    elif not is_valid:
        st.warning("⚠️ Thumbnail must be in 16:9 format.")
    else:
        with st.spinner("Analyzing..."):
            result = generate_prediction(title_input, image)

        st.success("✅ Analysis complete!")

        # --- Suggestions ---
        st.subheader("💡 AI Suggestions")
        st.markdown(f"**📢 Improved Title:** `{result['suggested_title']}`")
        st.info(f"✍️ *Title Tip:* {result['tip']}")
        st.info(f"🖼️ *Thumbnail Tip:* {result['thumbnail_tip']}")

        # --- Top YouTube Videos ---
        st.subheader("📈 Top Similar Videos")
        for video in result["top_videos"][:3]:  # Show only 3 videos
            title = video.get("title", "Untitled")
            url = video.get("url")
            if url:
                st.markdown(f"- **[{title}]({url})**")
            else:
                st.markdown(f"- **{title}**")

st.divider()
st.caption("Made by [@valm10](https://github.com/valm10) · Powered by Streamlit")
