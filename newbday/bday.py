import streamlit as st
import base64
from PIL import Image
import time

st.set_page_config(page_title="Pavani's Birthday Gift 🎁", layout="centered")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #ff69b4;
        font-size: 3em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    
    .subtitle {
        text-align: center;
        color: #ff1493;
        font-size: 1.5em;
        margin-bottom: 30px;
    }
    
    .final-message {
        text-align: center;
        color: #ff69b4;
        font-size: 2em;
        margin-top: 30px;
        padding: 20px;
        background: linear-gradient(45deg, #ffeef8, #fff0f8);
        border-radius: 15px;
        border: 2px solid #ff69b4;
    }
    
    .slideshow-container {
        position: relative;
        margin: 20px 0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">🎉 Happy Birthday Pavani 🎉</h1>', unsafe_allow_html=True)

# Intro Message
st.markdown('<h3 class="subtitle">A Small Gift On Your Precious Day 💝</h3>', unsafe_allow_html=True)

# Background Music Function
def autoplay_audio(file_path: str):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
        <audio autoplay loop controls style="width: 100%;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        Your browser does not support the audio element.
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)
    except FileNotFoundError:
        st.info("🎵 Add your music.mp3 file to enable background music!")

# Try to load background music
autoplay_audio("music.mp3")

# Image slideshow with session state
# Option 1: Put images in same folder as this script
# Option 2: Create an 'images' folder and update paths below
# Option 3: Use full file paths

image_paths = [
    "images/IMG-20250308-WA0040.jpg",  # Update these paths
    "images/IMG-20250313-WA0031.jpg", 
    "images/IMG_20250323_142607263.jpg",
    "images/IMG_20250323_142522740.jpg",
    "images/IMG_20250323_143639041_HDR.jpg",
    "images/IMG-20250324-WA0088.jpg"
]

# Alternative: Let user upload images directly
uploaded_files = st.file_uploader(
    "Or upload images here if files are missing:", 
    accept_multiple_files=True,
    type=['jpg', 'jpeg', 'png']
)

if uploaded_files:
    image_paths = uploaded_files

# Initialize session state for slideshow
if 'current_image' not in st.session_state:
    st.session_state.current_image = 0
if 'auto_advance' not in st.session_state:
    st.session_state.auto_advance = False

# Slideshow controls
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("⏮️ Previous"):
        st.session_state.current_image = (st.session_state.current_image - 1) % len(image_paths)

with col2:
    if st.button("⏸️ Pause" if st.session_state.auto_advance else "▶️ Play"):
        st.session_state.auto_advance = not st.session_state.auto_advance

with col3:
    if st.button("⏭️ Next"):
        st.session_state.current_image = (st.session_state.current_image + 1) % len(image_paths)

with col4:
    if st.button("🔄 Restart"):
        st.session_state.current_image = 0

# Display current image
if image_paths:
    try:
        current_path = image_paths[st.session_state.current_image]
        
        # Handle both file paths and uploaded files
        if isinstance(current_path, str):
            img = Image.open(current_path)
        else:
            img = Image.open(current_path)
        
        # Display image with container styling
        st.markdown('<div class="slideshow-container">', unsafe_allow_html=True)
        st.image(img, use_column_width=True, caption=f"Memory {st.session_state.current_image + 1} of {len(image_paths)} 📸")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Progress bar
        progress = (st.session_state.current_image + 1) / len(image_paths)
        st.progress(progress)
        
    except FileNotFoundError:
        st.error(f"Image not found: {current_path}")
        st.info("📁 **How to fix this:**\n1. Create an 'images' folder next to your Python script\n2. Put all photos in that folder\n3. OR use the file uploader above")
    except Exception as e:
        st.error(f"Error loading image: {e}")
else:
    st.info("No images found. Please upload some photos using the file uploader above!")

# Auto-advance functionality
if st.session_state.auto_advance:
    time.sleep(2)  # Wait 2 seconds
    st.session_state.current_image = (st.session_state.current_image + 1) % len(image_paths)
    st.rerun()

# Display all images as thumbnails
if image_paths:
    st.markdown("### 📷 All Memories")
    cols = st.columns(3)
    for i, path in enumerate(image_paths):
        try:
            if isinstance(path, str):
                img = Image.open(path)
            else:
                img = Image.open(path)
            
            with cols[i % 3]:
                if st.button(f"View Image {i+1}", key=f"thumb_{i}"):
                    st.session_state.current_image = i
                st.image(img, use_column_width=True)
        except FileNotFoundError:
            with cols[i % 3]:
                st.error(f"Missing: {path}")
        except Exception as e:
            with cols[i % 3]:
                st.error(f"Error: {e}")

# Final Message
st.markdown("""
<div class="final-message">
    💖 Stay Happy Always Pavani 💖<br>
    Wishing You Love, Luck and Light ✨<br>
    <small>Hope this year brings you everything wonderful! 🌟</small>
</div>
""", unsafe_allow_html=True)

# Add some birthday emojis
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 2em;'>🎂🎈🎁🌟💝🎉🎊✨</p>", unsafe_allow_html=True)
