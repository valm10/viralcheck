import streamlit as st
from PIL import Image
from utils.image_utils import check_aspect_ratio


#Page config (tab title and layout)
st.set_page_config(
    page_title="ViralCheck - Youtube Analyzer",
    page_icon="📈",
    layout="centered"
)

#App title and description
st.title("🚀 ViralCheck")
st.caption("Predict and improve your YouTube video virality.")

st.divider()

#Header for inputs
st.header("🎬 Video Details")

#Title input from user
title_input = st.text_input("📌 Enter your YouTube video title")

#Thumbnail upload
thumbnail_file = st.file_uploader("🖼️ Upload your thumbnail image", type=["jpg", "jpeg", "png"])

#Show preview if image uploaded

if thumbnail_file:
    image = Image.open(thumbnail_file)
    is_valid, width, height = check_aspect_ratio(image)

    st.image(image, caption="Thumbnail Preview", use_column_width=True)

    if is_valid:
        st.success("✅ Thumbnail is in 16:9 format.")
    else:
        st.warning("⚠️ Thumbnail is NOT 16:9 (e.g., 1280x720).")
