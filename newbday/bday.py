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
    "🌺 You are loved more than words can say"
]

# -- Orientation fix
def fix_orientation(img):
    try:
        if hasattr(img, '_getexif'):
            img_no_exif = Image.new(img.mode, img.size)
            img_no_exif.putdata(list(img.getdata()))
            return img_no_exif
        return img
    except Exception:
        return img

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
uploaded_files = st.file_uploader("📸 Upload Birthday Pictures", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
uploaded_music = st.file_uploader("🎵 Upload Birthday Song", type=["mp3", "wav", "ogg"])

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.success(f"Uploaded {len(uploaded_files)} pictures.")

if uploaded_music:
    st.session_state.uploaded_music = uploaded_music
    st.success(f"Uploaded music: {uploaded_music.name}")

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
            <div class="music-indicator">🎵 {st.session_state.uploaded_music.name}</div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Music error: {e}")

    # -- Slideshow
    if st.session_state.slideshow_active:
        try:
            img = Image.open(st.session_state.uploaded_files[st.session_state.current_image])
            img = fix_orientation(img)

            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            img_b64 = base64.b64encode(buffer.getvalue()).decode()

            quote = QUOTES[st.session_state.current_image % len(QUOTES)]

            st.markdown(f"""
            <div style="position: relative; max-width: 700px; margin: auto; border-radius: 15px; overflow: hidden;">
                <img src="data:image/jpeg;base64,{img_b64}" style="width: 100%; border-radius: 15px;">
                <div style="
                    position: absolute;
                    bottom: 0;
                    width: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    color: #fff;
                    font-size: 1.4em;
                    padding: 20px;
                    text-align: center;
                    font-style: italic;
                    font-weight: bold;">
                    {quote}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Progress
            st.progress((st.session_state.current_image + 1) / len(st.session_state.uploaded_files))

            time.sleep(4)
            st.session_state.current_image += 1

            if st.session_state.current_image >= len(st.session_state.uploaded_files):
                st.session_state.slideshow_active = False
                st.session_state.current_image = 0

                st.markdown(f"""
                <div class="final-message">
                    🎂 Happy Birthday, Pavani! 🎂<br><br>
                    💖 May your day be filled with smiles, hugs, cake,<br>
                    and unforgettable memories! 💖<br><br>
                    🎊 Keep shining, keep smiling, and keep spreading joy 🎊
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    if st.button("🔁 WATCH AGAIN"):
                        st.session_state.slideshow_active = True
                        st.session_state.current_image = 0
                        st.rerun()
            else:
                st.rerun()
        except Exception as e:
            st.error(f"Error displaying image: {e}")

elif not uploaded_files or not uploaded_music:
    st.info("📸 Upload pictures and 🎵 music to start the slideshow.")

# -- Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ff69b4;'>Made with ❤️ for Pavani's Birthday</p>", unsafe_allow_html=True)
