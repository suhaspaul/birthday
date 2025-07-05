import streamlit as st
import base64
from PIL import Image
import time
import random

st.set_page_config(page_title="🎉 Birthday Slideshow", layout="centered")

# Simple and clean CSS
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
    
    .control-button {
        background: linear-gradient(45deg, #ff69b4, #ff1493);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
        font-size: 1.2em;
        font-weight: bold;
        margin: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .control-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 105, 180, 0.4);
    }
    
    .upload-section {
        background: linear-gradient(45deg, #f0f8ff, #e6f3ff);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        border: 2px dashed #4169e1;
        text-align: center;
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
</style>
""", unsafe_allow_html=True)

# Beautiful quotes for each picture
BEAUTIFUL_QUOTES = [
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

# Initialize session state
if 'slideshow_active' not in st.session_state:
    st.session_state.slideshow_active = False
if 'current_image' not in st.session_state:
    st.session_state.current_image = 0
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
if 'uploaded_music' not in st.session_state:
    st.session_state.uploaded_music = None

# Header
st.markdown('<h1 class="main-title">🎉 Birthday Slideshow Creator 🎉</h1>', unsafe_allow_html=True)

# Step 1: Upload Pictures
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("### 📸 Step 1: Upload Birthday Pictures")
uploaded_files = st.file_uploader(
    "Choose pictures for the birthday slideshow:",
    accept_multiple_files=True,
    type=['jpg', 'jpeg', 'png', 'bmp'],
    help="Upload multiple photos to create a beautiful slideshow"
)

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.success(f"✅ {len(uploaded_files)} pictures uploaded successfully!")

# Step 2: Upload Music
st.markdown("### 🎵 Step 2: Upload Birthday Music")
uploaded_music = st.file_uploader(
    "Choose a birthday song:",
    type=['mp3', 'wav', 'ogg'],
    help="Upload a music file to play during the slideshow"
)

if uploaded_music:
    st.session_state.uploaded_music = uploaded_music
    st.success(f"✅ Music '{uploaded_music.name}' uploaded successfully!")

st.markdown('</div>', unsafe_allow_html=True)

# Step 3: Start Slideshow
if st.session_state.uploaded_files and st.session_state.uploaded_music:
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.slideshow_active:
            if st.button("🎬 START BIRTHDAY SLIDESHOW 🎬", key="start_slideshow"):
                st.session_state.slideshow_active = True
                st.session_state.current_image = 0
                st.rerun()
        else:
            if st.button("⏹️ STOP SLIDESHOW", key="stop_slideshow"):
                st.session_state.slideshow_active = False
                st.rerun()

    # Auto-playing music when slideshow starts
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
            st.error(f"Error playing music: {e}")

    # Slideshow Display
    if st.session_state.slideshow_active:
        st.markdown('<div class="slideshow-container">', unsafe_allow_html=True)
        
        try:
            # Display current image
            current_file = st.session_state.uploaded_files[st.session_state.current_image]
            img = Image.open(current_file)
            
            # Display image
            st.image(img, use_container_width=True, caption=f"Photo {st.session_state.current_image + 1} of {len(st.session_state.uploaded_files)}")
            
            # Display beautiful quote for current image
            current_quote = BEAUTIFUL_QUOTES[st.session_state.current_image % len(BEAUTIFUL_QUOTES)]
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
                🎂 Happy Birthday! 🎂<br><br>
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
                if st.button("🔄 WATCH SLIDESHOW AGAIN 🔄", key="restart_slideshow"):
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
        <h2 style="color: #ff1493;">🎈 Welcome to Birthday Slideshow Creator! 🎈</h2>
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

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 2em;'>🎂🎈🎁🌟💝🎉🎊✨</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ff69b4; font-size: 1.2em;'>Made with ❤️ for special birthdays</p>", unsafe_allow_html=True)
