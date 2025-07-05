import streamlit as st
import base64
from PIL import Image
import time
import os

st.set_page_config(page_title="Pavani's Birthday Gift 🎁", layout="centered")

# Title
st.markdown(
    "<h1 style='text-align: center; color: #ff69b4;'>🎉 Happy Birthday Pavani 🎉</h1>",
    unsafe_allow_html=True
)

# Intro Message
st.markdown(
    "<h3 style='text-align: center;'>A Small Gift On Your Precious Day 💝</h3><br>", 
    unsafe_allow_html=True
)

# Background Music
def autoplay_audio(file_path: str):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
        <audio autoplay loop>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)
    else:
        st.warning(f"🎵 Music file not found: {file_path}")

autoplay_audio("bdaysong.mp3")

# Image Slideshow
image_paths = [
    "IMG-20250308-WA0040.jpg",
    "IMG-20250313-WA0031.jpg",
    "IMG_20250323_142607263.jpg",
    "IMG_20250323_142522740.jpg",
    "IMG_20250323_143639041_HDR.jpg",
    "IMG-20250324-WA0088.jpg"
]

for path in image_paths:
    if os.path.exists(path):
        img = Image.open(path)
        st.image(img, use_column_width=True)
        time.sleep(1.5)
    else:
        st.warning(f"⚠️ Image not found: {path}")

# Final Message
st.markdown(
    "<h2 style='text-align: center;'>💖 Stay Happy Always Pavani 💖<br>Wishing You Love, Luck and Light ✨</h2>",
    unsafe_allow_html=True
)
