import streamlit as st
from PIL import Image, UnidentifiedImageError
from utils.image_utils import check_aspect_ratio
from utils.openai_helper import generate_prediction

#Page Configuration
st.set_page_config(
    page_title="ViralCheck - YouTube Analyzer",
    page_icon="📈",
    layout="centered"
)

#App Title
st.title("🚀 ViralCheck")
st.caption("Boost your YouTube video's performance with AI powered title and thumbnail suggestions.")

st.divider()

#User Input Section 
st.header("🎬 Video Details")

#Input for video title
title_input = st.text_input("📌 Enter your YouTube video title")

#File uploader for thumbnail image
thumbnail_file = st.file_uploader(
    "🖼️ Upload your video thumbnail (JPG or PNG)",
    type=["jpg", "jpeg", "png"]
)

image = None
is_valid = False

#Process the uploaded thumbnail
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

# --- Analysis Section ---
st.header("📊 Viral Prediction")

# Analyze button
if st.button("🔍 Analyze with AI"):
    if not title_input:
        st.warning("⚠️ Please provide a video title.")
    elif not thumbnail_file or not image:
        st.warning("⚠️ Please upload a valid thumbnail image.")
    elif not is_valid:
        st.warning("⚠️ Please upload a thumbnail in 16:9 format before analyzing.")
    else:
        with st.spinner("Analyzing..."):
            result = generate_prediction(title_input, image)

        st.success("✅ Analysis complete!")

        #Display AI suggestions
        st.subheader("💡 AI Suggestions")
        st.markdown(f"**📢 Improved Title:** `{result['suggested_title']}`")
        st.info(f"✍️ *Title Tip:* {result['tip']}")
        st.info(f"🖼️ *Thumbnail Tip:* {result['thumbnail_tip']}")

        #Display top similar videos
        st.subheader("📈 Top Similar Videos")
        for video in result["top_videos"]:
            st.markdown(f"- **{video['title']}** — Score: {video['score']}/100")

        for video in result["top_videos"]:
            st.markdown(f"""
            **[{video['title']}]({video['url']})**  
            By: `{video['channel']}`  
            👁️ {video['views']:,} views  
---
""")


st.divider()
st.caption("Made by [@valm10](https://github.com/valm10) · Powered by Streamlit")