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
    "💞 Friends like you are rare and precious 💫",
    "🌟 Every memory with you is a beautiful chapter in my life 📖",
    "💖 You’re not just a friend, you’re family 💝",
    "🎈 Our bond is built on laughter, love, and endless talks 💬",
    "🌸 I’m so lucky to have a friend like you in my life 🍀",
    "💕 No distance, no time, no reason can break our bond 🔗",
    "💫 True friendship isn't about being inseparable, it's about being connected by heart 🫶",
    "💌 You're my favorite person to share my madness with 😜",
    "🎉 Cheers to the memories we've made and the ones still to come 🥂",
    "🫂 You’re my happy place when the world feels too heavy 💗"
]


# -- Orientation fix
from PIL import ExifTags

def fix_orientation(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = img._getexif()

        if exif is not None:
            orientation_value = exif.get(orientation, None)

            if orientation_value == 3:
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:
                img = img.rotate(90, expand=True)
    except Exception:
        pass
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
                🎂 Happy Birthday to my cute sweet Pavani 🎂<br><br>
                💝 This beautiful slideshow was created especially for you<br>
                with lots of love and affection! 💝<br><br>
                🌟 A small bday gift to my DUMBU FELLOW<br>
                this special day in a memorable way! 🌟<br><br>
                💖 May your birthday be filled with joy, laughter,<br>
                and all the happiness you deserve! 💖<br><br>
                🎉 Here's to another amazing year ahead!,hope Our BOND continues..... 🎉
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
