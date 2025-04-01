import streamlit as st
from PIL import Image
from utils.image_utils import check_aspect_ratio
from utils.openai_helper import generate_prediction

# --- Streamlit Config ---
st.set_page_config(
    page_title="ViralCheck - YouTube Analyzer",
    page_icon="📈",
    layout="centered"
)

# --- Sidebar Branding ---
def render_sidebar():
    st.image("static/icon.png", width=180)
    st.markdown("## 🎥 ViralCheck")
    st.markdown("**Predict your YouTube video's viral potential using AI.**")
    st.markdown("Made with ❤️ by [@valm10](https://github.com/valm10)")

# --- App Header ---
st.title("🚀 ViralCheck - YouTube Viral Analyzer")
st.caption("Upload your title and thumbnail. We'll suggest improvements and estimate virality.")
st.divider()

# --- Input Section ---
st.header("🎬 Video Details")
title_input = st.text_input("📌 YouTube Video Title")
thumbnail_input = st.file_uploader("🖼️ Upload Thumbnail (JPG/PNG)", type=["jpg", "jpeg", "png"])

image = None
is_valid = False

if thumbnail_input:
    image = Image.open(thumbnail_input)
    is_valid, width, height = check_aspect_ratio(image)
    st.image(image, caption=f"Preview ({width}x{height})", use_container_width=True)

    if not is_valid:
        st.warning("⚠️ Not a 16:9 ratio! Recommended: 1280x720 (16:9)")
    else:
        st.success("✅ Thumbnail meets the 16:9 YouTube standard.")

st.divider()

# --- Analysis Section ---
st.header("📊 Viral Prediction")

if st.button("🚀 Analyze Video"):
    if not title_input or not thumbnail_input:
        st.warning("⚠️ Please provide both a title and thumbnail.")
    elif not is_valid:
        st.warning("⚠️ Please use a thumbnail with a 16:9 ratio before analyzing.")
    else:
        st.success("✅ Analyzing your video...")

        result = generate_prediction(title_input, image)

        st.subheader("🔮 Prediction Results")
        st.metric(label="Virality Score", value="⚡ High Potential", delta="↑ Likely to trend")

        st.image(thumbnail_input, caption="Your Thumbnail", use_container_width=True)

        st.subheader("✨ AI Suggestions")
        st.markdown(f"**📢 Improved Title:** `{result['suggested_title']}`")
        st.info(f"✍️ *Title Tip:* {result['tip']}")
        st.info(f"🖼️ *Thumbnail Tip:* {result['thumbnail_tip']}")

        st.subheader("📈 Similar Top-Performing Videos")
        for video in result["top_videos"]:
            st.markdown(f"- **{video['title']}** — Score: {video['score']}/100")

st.divider()
st.caption("Built using Streamlit + OpenAI • Powered by [@valm10](https://github.com/valm10)")
