# Import Streamlit
import streamlit as st

# Import Pillow to handle image files
from PIL import Image

# Import helper utilities
from utils.image_utils import check_aspect_ratio
from utils.openai_helper import generate_prediction


# <-- App Configuration -->
st.set_page_config(
    page_title="ViralCheck - YouTube Viral Analyzer",
    page_icon="📈",
    layout="centered"
)

st.title("Viral Check - YouTube Viral Analyser")
st.caption("Predict and improve your video’s viral potential using AI.")
st.divider()

# <-- Input Section -->
st.header("🎬 Video Details")
title_input = st.text_input("📌 Your YouTube Video Title:")

thumbnail_input = st.file_uploader(
    "🖼️ Your YouTube Thumbnail (JPG, PNG):",
    type=["jpg", "jpeg", "png"]
)

# Validate uploaded image
image = None
is_valid = False
if thumbnail_input is not None:
    image = Image.open(thumbnail_input)
    is_valid, width, height = check_aspect_ratio(image)

    if not is_valid:
        st.warning("⚠️ This image is not in the recommended 16:9 YouTube thumbnail format (e.g. 1280x720).")
    else:
        st.success("✅ Thumbnail meets the 16:9 ratio requirement.")

    st.image(image, caption=f"Thumbnail Preview ({width}x{height})", use_container_width=True)

# <-- Analysis Section -->
st.divider()
st.header("📊 Viral Prediction")

if st.button("🚀 Check Virality"):
    if not title_input or not thumbnail_input:
        st.warning("⚠️ Please provide both a title and a thumbnail.")
    elif not is_valid:
        st.warning("⚠️ Please upload a valid 16:9 thumbnail before analyzing.")
    else:
        # Run AI-powered or fallback prediction
        result = generate_prediction(title_input, image)

        # Display analysis results
        st.success("✅ Analysis complete!")

        st.subheader("🔮 AI Prediction")
        st.metric("Virality Score", "AI Prediction", delta="↑ ⚡ High Potential")

        st.image(thumbnail_input, caption="Your Thumbnail", use_container_width=True)

        st.subheader("✨ Suggested Improvements")
        st.markdown(f"**📢 Improved Title:** `{result['suggested_title']}`")
        st.info(f"✍️ *Title Tip:* {result['tip']}")
        st.info(f"🖼️ *Thumbnail Tip:* {result['thumbnail_tip']}")

        st.subheader("📈 Top-Performing Similar Videos")
        for video in result['top_videos']:
            st.markdown(f"- **{video['title']}** – *Score: {video['score']}/100*")

# Footer
st.divider()
st.caption("Made with ❤️ by [@valm10](https://github.com/valm10) · Powered by Streamlit")
