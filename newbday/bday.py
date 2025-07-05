import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import time
import random

st.set_page_config(page_title="🎉 Pavani's Birthday Gift", layout="centered")

# -- Styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #ff69b4;
        font-size: 3em;
        margin-bottom: 30px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .music-indicator {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(255,105,180,0.9);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        z-index: 1000;
        animation: bounce 2s infinite;
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }

    .final-message {
        text-align: center;
        color: #ff69b4;
        font-size: 2em;
        margin-top: 40px;
        padding: 30px;
        background: linear-gradient(45deg, #ffeef8, #fff0f8);
        border-radius: 20px;
        border: 3px solid #ff69b4;
        animation: glow 3s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { box-shadow: 0 0 15px #ff69b4; }
        to { box-shadow: 0 0 25px #ff69b4; }
    }

    .slideshow-container {
        text-align: center;
        margin: 30px 0;
        padding: 20px;
        background: linear-gradient(45deg, #ffeef8, #fff0f8);
        border-radius: 15px;
        border: 3px solid #ff69b4;
    }

    .quote-text {
        font-size: 1.5em;
        color: #ff1493;
        font-style: italic;
        margin: 20px 0;
        padding: 15px;
        background: rgba(255,255,255,0.8);
        border-radius: 10px;
        border-left: 5px solid #ff69b4;
    }

    .upload-section {
        background: linear-gradient(45deg, #f0f8ff, #e6f3ff);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        border: 2px dashed #4169e1;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -- Quotes
QUOTES = [
    "💫 Every moment with you is a precious gift",
    "🌟 Your smile lights up our world",
    "✨ Life is more beautiful because you're in it",
    "🎈 You bring joy to everyone around you",
    "💝 Another year of wonderful memories with you",
    "🌈 You make every day brighter and better",
    "🎉 Celebrating the amazing person you are",
    "💖 Your kindness touches every heart",
    "🎂 May your special day be filled with love",
    "🌺 You are loved more than words can say",
    "⭐ You make the world a better place",
    "🎊 Here's to another year of happiness",
    "🌹 Your laughter is music to our ears",
    "💐 You deserve all the love in the world",
    "🎁 You are our greatest blessing"
]

# Function to fix image orientation (prevent rotation)
def fix_image_orientation(image):
    """
    Fix image orientation by removing EXIF orientation data
    and ensuring the image is displayed straight
    """
    try:
        # Remove EXIF data that might cause rotation
        if hasattr(image, '_getexif'):
            # Create a new image without EXIF data
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(list(image.getdata()))
            return image_without_exif
        else:
            return image
    except Exception:
        # If there's any error, return the original image
        return image

# -- Session states
if 'slideshow_active' not in st.session_state:
    st.session_state.slideshow_active = False
if 'current_image' not in st.session_state:
    st.session_state.current_image = 0
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
if 'uploaded_music' not in st.session_state:
    st.session_state.uploaded_music = None

# -- Title
st.markdown('<h1 class="main-title">🎉 Happy Birthday Pavani 🎉</h1>', unsafe_allow_html=True)
st.markdown("### 💝 A Small Gift On Your Precious Day")

# -- Upload section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("### 📸 Upload Birthday Pictures")
uploaded_files = st.file_uploader(
    "Choose pictures for the birthday slideshow:",
    accept_multiple_files=True,
    type=["jpg", "jpeg", "png", "bmp"],
    help="Upload multiple photos to create a beautiful slideshow"
)

st.markdown("### 🎵 Upload Birthday Song")
uploaded_music = st.file_uploader(
    "Choose a birthday song:",
    type=["mp3", "wav", "ogg"],
    help="Upload a music file to play during the slideshow"
)

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.success(f"✅ {len(uploaded_files)} pictures uploaded successfully!")

if uploaded_music:
    st.session_state.uploaded_music = uploaded_music
    st.success(f"✅ Music '{uploaded_music.name}' uploaded successfully!")

st.markdown('</div>', unsafe_allow_html=True)

# -- Slideshow Controls
if st.session_state.uploaded_files and st.session_state.uploaded_music:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if not st.session_state.slideshow_active:
            if st.button("🎬 START SLIDESHOW"):
                st.session_state.slideshow_active = True
                st.session_state.current_image = 0
                st.rerun()
        else:
            if st.button("⏹️ STOP SLIDESHOW"):
                st.session_state.slideshow_active = False
                st.rerun()

    # -- Music
    if st.session_state.slideshow_active and st.session_state.uploaded_music:
        try:
            audio_bytes = st.session_state.uploaded_music.read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f"""
            <audio autoplay loop style="display: none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            <div class="music-indicator">🎵 Playing: {st.session_state.uploaded_music.name}</div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Music error: {e}")

    # -- Slideshow
    if st.session_state.slideshow_active:
        st.markdown('<div class="slideshow-container">', unsafe_allow_html=True)
        
        try:
            # Display current image
            current_file = st.session_state.uploaded_files[st.session_state.current_image]
            img = Image.open(current_file)
            
            # Fix image orientation to prevent rotation
            img = fix_image_orientation(img)
            
            # Display image straight without any rotation
            st.image(img, use_container_width=True, caption=f"Photo {st.session_state.current_image + 1} of {len(st.session_state.uploaded_files)}")
            
            # Display beautiful quote for current image
            current_quote = QUOTES[st.session_state.current_image % len(QUOTES)]
            st.markdown(f'<div class="quote-text">{current_quote}</div>', unsafe_allow_html=True)
            
            # Progress bar
            progress = (st.session_state.current_image + 1) / len(st.session_state.uploaded_files)
            st.progress(progress)
            
        except Exception as e:
            st.error(f"Error displaying image: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-advance slideshow
        time.sleep(4)  # Show each image for 4 seconds
        st.session_state.current_image += 1
        
        # Check if slideshow is complete
        if st.session_state.current_image >= len(st.session_state.uploaded_files):
            st.session_state.slideshow_active = False
            st.session_state.current_image = 0
            
            # Show final birthday message
            st.markdown(f"""
            <div class="final-message">
                🎂 Happy Birthday Pavani! 🎂<br><br>
                💝 This beautiful slideshow was created especially for you<br>
                with lots of love and affection! 💝<br><br>
                🌟 You mean the world to us and we wanted to celebrate<br>
                this special day in a memorable way! 🌟<br><br>
                💖 May your birthday be filled with joy, laughter,<br>
                and all the happiness you deserve! 💖<br><br>
                🎉 Here's to another amazing year ahead! 🎉
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-restart option
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 WATCH SLIDESHOW AGAIN 🔄"):
                    st.session_state.slideshow_active = True
                    st.session_state.current_image = 0
                    st.rerun()
        else:
            st.rerun()

elif st.session_state.uploaded_files and not st.session_state.uploaded_music:
    st.warning("🎵 Please upload music to start the slideshow!")

elif not st.session_state.uploaded_files and st.session_state.uploaded_music:
    st.warning("📸 Please upload pictures to start the slideshow!")

else:
    # Welcome message
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: linear-gradient(45deg, #ffeef8, #fff0f8); 
                border-radius: 15px; margin: 20px 0; border: 3px solid #ff69b4;">
        <h2 style="color: #ff1493;">🎈 Welcome to Pavani's Birthday Slideshow! 🎈</h2>
        <p style="font-size: 1.3em; color: #ff69b4;">Create a magical birthday slideshow with music!</p>
        <br>
        <p style="font-size: 1.1em; color: #ff1493;"><strong>How it works:</strong></p>
        <div style="text-align: left; display: inline-block; color: #c71585; font-size: 1.1em;">
            <p>1. 📸 Upload birthday pictures</p>
            <p>2. 🎵 Upload a birthday song</p>
            <p>3. 🎬 Click start to begin the slideshow</p>
            <p>4. 🎉 Enjoy the beautiful slideshow with music!</p>
        </div>
        <br>
        <p style="font-size: 1.2em; color: #ff69b4;">
            Each picture will have a beautiful message! 💝
        </p>
    </div>
    """, unsafe_allow_html=True)

# -- Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 2em;'>🎂🎈🎁🌟💝🎉🎊✨</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ff69b4;font-size: 1.2em;'>Made with ❤️ for Pavani's Birthday</p>", unsafe_allow_html=True)
