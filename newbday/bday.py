import streamlit as st
import base64
from PIL import Image, ImageEnhance, ImageFilter
import time
import random
from datetime import datetime
import io

st.set_page_config(
    page_title="🎉 Birthday Gift Creator", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with more animations and effects
st.markdown("""
<style>
    .main-title {
        text-align: center;
        background: linear-gradient(45deg, #ff69b4, #ff1493, #c71585);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        animation: rainbow 3s ease-in-out infinite alternate;
    }
    
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(180deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    .subtitle {
        text-align: center;
        color: #ff1493;
        font-size: 1.8em;
        margin-bottom: 30px;
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
        font-size: 2.2em;
        margin-top: 30px;
        padding: 25px;
        background: linear-gradient(135deg, #ffeef8, #fff0f8, #ffe4e6);
        border-radius: 20px;
        border: 3px solid #ff69b4;
        animation: glow 4s ease-in-out infinite alternate;
        position: relative;
        overflow: hidden;
    }
    
    .final-message::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    @keyframes glow {
        from { 
            box-shadow: 0 0 15px #ff69b4, 0 0 25px #ff69b4; 
            transform: scale(1);
        }
        to { 
            box-shadow: 0 0 25px #ff69b4, 0 0 35px #ff69b4; 
            transform: scale(1.02);
        }
    }
    
    .slideshow-container {
        position: relative;
        margin: 20px 0;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ff69b4, #ff1493);
        padding: 5px;
        animation: slideshow-glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes slideshow-glow {
        from { box-shadow: 0 8px 32px rgba(255,105,180,0.4); }
        to { box-shadow: 0 12px 40px rgba(255,105,180,0.6); }
    }
    
    .image-container {
        position: relative;
        border-radius: 15px;
        overflow: hidden;
        background: white;
        animation: image-slide-in 1s ease-out;
    }
    
    @keyframes image-slide-in {
        from { 
            opacity: 0; 
            transform: translateX(100px) rotateY(45deg);
        }
        to { 
            opacity: 1; 
            transform: translateX(0) rotateY(0deg);
        }
    }
    
    .image-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            45deg,
            rgba(255,105,180,0.1) 0%,
            transparent 25%,
            transparent 75%,
            rgba(255,20,147,0.1) 100%
        );
        pointer-events: none;
        animation: overlay-pulse 4s ease-in-out infinite;
    }
    
    @keyframes overlay-pulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.1; }
    }
    
    .image-border-effect {
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #ff69b4, #ff1493, #c71585, #ff69b4);
        border-radius: 17px;
        animation: border-rotate 3s linear infinite;
        z-index: -1;
    }
    
    @keyframes border-rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .beautiful-quote {
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.9);
        padding: 15px 25px;
        border-radius: 25px;
        font-style: italic;
        font-size: 1.2em;
        color: #ff1493;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        animation: quote-fade-in 2s ease-in-out;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255,105,180,0.3);
    }
    
    @keyframes quote-fade-in {
        from { 
            opacity: 0; 
            transform: translateX(-50%) translateY(20px);
        }
        to { 
            opacity: 1; 
            transform: translateX(-50%) translateY(0);
        }
    }
    
    .sparkle-effect {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        pointer-events: none;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(255,255,255,0.8) 2px, transparent 2px),
            radial-gradient(circle at 80% 70%, rgba(255,255,255,0.6) 1px, transparent 1px),
            radial-gradient(circle at 60% 20%, rgba(255,255,255,0.4) 1px, transparent 1px),
            radial-gradient(circle at 30% 80%, rgba(255,255,255,0.7) 2px, transparent 2px);
        background-size: 200px 200px, 150px 150px, 100px 100px, 250px 250px;
        animation: sparkle-twinkle 4s ease-in-out infinite;
    }
    
    @keyframes sparkle-twinkle {
        0%, 100% { opacity: 0; }
        50% { opacity: 1; }
    }
    
    .music-note {
        position: fixed;
        font-size: 2em;
        color: #ff69b4;
        animation: float-notes 6s ease-in-out infinite;
        z-index: 1000;
        pointer-events: none;
    }
    
    @keyframes float-notes {
        0% { 
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { 
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }
    }
    
    .upload-section {
        background: linear-gradient(135deg, #f0f8ff, #e6f3ff, #ddeeff);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 3px dashed #4169e1;
        animation: section-glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes section-glow {
        from { border-color: #4169e1; }
        to { border-color: #ff69b4; }
    }
    
    .control-buttons {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 25px 0;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #ff69b4, #ff1493);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 25px;
        font-weight: bold;
        font-size: 1.1em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255,105,180,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(255,105,180,0.5);
        background: linear-gradient(45deg, #ff1493, #c71585);
    }
    
    .auto-music-indicator {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(255,105,180,0.9);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        animation: music-pulse 2s ease-in-out infinite;
        z-index: 1000;
    }
    
    @keyframes music-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
</style>
""", unsafe_allow_html=True)

# Beautiful quotes for slideshow
BEAUTIFUL_QUOTES = [
    "💫 Every picture tells a story of love and joy",
    "🌟 Memories are the treasures of the heart",
    "✨ Life is a beautiful collection of moments",
    "🎈 Each smile captured is a gift to treasure",
    "💝 Love grows stronger with every memory shared",
    "🌈 Beautiful moments deserve beautiful celebrations",
    "🎉 Today we celebrate the joy you bring to our lives",
    "💖 Your happiness lights up every photograph",
    "🎂 Another year of wonderful memories to cherish",
    "🌺 May your special day be filled with magic",
    "⭐ You make every moment sparkle with joy",
    "🎊 Celebrating the amazing person you are"
]

# Initialize session state
if 'current_image' not in st.session_state:
    st.session_state.current_image = 0
if 'auto_advance' not in st.session_state:
    st.session_state.auto_advance = False
if 'birthday_name' not in st.session_state:
    st.session_state.birthday_name = ""
if 'custom_message' not in st.session_state:
    st.session_state.custom_message = ""
if 'slideshow_speed' not in st.session_state:
    st.session_state.slideshow_speed = 4
if 'image_effects' not in st.session_state:
    st.session_state.image_effects = True
if 'auto_music' not in st.session_state:
    st.session_state.auto_music = True

# Create floating music notes
def create_floating_notes():
    notes = ['🎵', '🎶', '🎼', '♪', '♫', '♬']
    for i in range(3):
        note = random.choice(notes)
        left_pos = random.randint(10, 90)
        delay = random.uniform(0, 2)
        st.markdown(f"""
        <div class="music-note" style="left: {left_pos}%; animation-delay: {delay}s;">
            {note}
        </div>
        """, unsafe_allow_html=True)

# Header Section
st.markdown('<h1 class="main-title">🎉 Birthday Gift Creator 🎉</h1>', unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.markdown("### 🎛️ Slideshow Settings")
    
    st.session_state.slideshow_speed = st.slider(
        "⏱️ Slideshow Speed (seconds)", 
        min_value=2, max_value=10, 
        value=st.session_state.slideshow_speed
    )
    
    st.session_state.image_effects = st.checkbox(
        "✨ Enable Image Effects", 
        value=st.session_state.image_effects
    )
    
    st.session_state.auto_music = st.checkbox(
        "🎵 Auto-play Music in Slideshow", 
        value=st.session_state.auto_music
    )
    
    st.markdown("### 🎨 Image Filters")
    brightness = st.slider("☀️ Brightness", 0.5, 2.0, 1.0, 0.1)
    contrast = st.slider("🔆 Contrast", 0.5, 2.0, 1.0, 0.1)
    saturation = st.slider("🌈 Saturation", 0.0, 2.0, 1.0, 0.1)

# Personalization Section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("### 🎈 Personalize Your Birthday Gift")

col1, col2 = st.columns(2)
with col1:
    birthday_name = st.text_input("🎂 Birthday Person's Name:", value=st.session_state.birthday_name, placeholder="Enter name here...")
    if birthday_name:
        st.session_state.birthday_name = birthday_name

with col2:
    custom_message = st.text_area("💝 Custom Birthday Message:", value=st.session_state.custom_message, placeholder="Write a special message...")
    if custom_message:
        st.session_state.custom_message = custom_message

st.markdown('</div>', unsafe_allow_html=True)

# Display personalized title
if st.session_state.birthday_name:
    st.markdown(f'<h2 class="subtitle">🎁 Happy Birthday {st.session_state.birthday_name}! 🎁</h2>', unsafe_allow_html=True)
else:
    st.markdown('<h3 class="subtitle">Upload Photos to Create a Beautiful Birthday Slideshow 📸</h3>', unsafe_allow_html=True)

# File Upload Section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("### 📷 Upload Birthday Photos")

uploaded_files = st.file_uploader(
    "Choose photos to create your birthday slideshow:",
    accept_multiple_files=True,
    type=['jpg', 'jpeg', 'png', 'bmp', 'gif'],
    help="You can upload multiple photos at once!"
)

# Music Upload
uploaded_music = st.file_uploader(
    "🎵 Upload Birthday Music (Optional):",
    type=['mp3', 'wav', 'ogg'],
    help="Upload a music file to play in the background"
)

st.markdown('</div>', unsafe_allow_html=True)

# Function to apply image effects
def apply_image_effects(img, brightness=1.0, contrast=1.0, saturation=1.0):
    if st.session_state.image_effects:
        # Apply brightness
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
        
        # Apply contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)
        
        # Apply saturation
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(saturation)
        
        # Add slight blur for dreamy effect
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return img

# Background Music with auto-play
music_html = ""
if uploaded_music and st.session_state.auto_music and st.session_state.auto_advance:
    try:
        audio_bytes = uploaded_music.read()
        b64 = base64.b64encode(audio_bytes).decode()
        music_html = f"""
        <audio autoplay loop style="display: none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <div class="auto-music-indicator">🎵 Playing: {uploaded_music.name}</div>
        """
        st.markdown(music_html, unsafe_allow_html=True)
        
        # Create floating notes when music is playing
        create_floating_notes()
        
    except Exception as e:
        st.error(f"Error loading music: {e}")

elif uploaded_music:
    try:
        audio_bytes = uploaded_music.read()
        b64 = base64.b64encode(audio_bytes).decode()
        music_html = f"""
        <audio controls style="width: 100%; margin: 20px 0;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(music_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading music: {e}")

# Main slideshow logic
if uploaded_files:
    # Reset current image if new files uploaded
    if len(uploaded_files) <= st.session_state.current_image:
        st.session_state.current_image = 0
    
    # Slideshow controls
    st.markdown('<div class="control-buttons">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("⏮️ Previous"):
            st.session_state.current_image = (st.session_state.current_image - 1) % len(uploaded_files)
    
    with col2:
        if st.button("⏸️ Pause" if st.session_state.auto_advance else "▶️ Play"):
            st.session_state.auto_advance = not st.session_state.auto_advance
    
    with col3:
        if st.button("⏭️ Next"):
            st.session_state.current_image = (st.session_state.current_image + 1) % len(uploaded_files)
    
    with col4:
        if st.button("🔄 Restart"):
            st.session_state.current_image = 0
    
    with col5:
        if st.button("🎲 Random"):
            st.session_state.current_image = random.randint(0, len(uploaded_files) - 1)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display current image with effects
    try:
        current_file = uploaded_files[st.session_state.current_image]
        img = Image.open(current_file)
        
        # Apply image effects
        enhanced_img = apply_image_effects(img, brightness, contrast, saturation)
        
        # Display image with beautiful container and effects
        st.markdown('<div class="slideshow-container">', unsafe_allow_html=True)
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.markdown('<div class="image-border-effect"></div>', unsafe_allow_html=True)
        
        # Convert enhanced image to display
        img_buffer = io.BytesIO()
        enhanced_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        st.image(enhanced_img, use_container_width=True, caption=f"✨ Memory {st.session_state.current_image + 1} of {len(uploaded_files)} ✨")
        
        # Add overlay effects
        st.markdown('<div class="image-overlay"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sparkle-effect"></div>', unsafe_allow_html=True)
        
        # Add beautiful quote
        current_quote = BEAUTIFUL_QUOTES[st.session_state.current_image % len(BEAUTIFUL_QUOTES)]
        st.markdown(f'<div class="beautiful-quote">{current_quote}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced progress bar
        progress = (st.session_state.current_image + 1) / len(uploaded_files)
        st.progress(progress)
        
        # Image details with styling
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0; padding: 15px; 
                    background: linear-gradient(45deg, #fff0f8, #ffeef8); 
                    border-radius: 15px; border: 2px solid #ff69b4;">
            <strong>📁 File:</strong> {current_file.name}<br>
            <strong>📏 Size:</strong> {enhanced_img.size[0]} x {enhanced_img.size[1]} pixels<br>
            <strong>🎨 Effects:</strong> {'Applied' if st.session_state.image_effects else 'None'}
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading image: {e}")
    
    # Auto-advance functionality with music
    if st.session_state.auto_advance:
        with st.empty():
            time.sleep(st.session_state.slideshow_speed)
        st.session_state.current_image = (st.session_state.current_image + 1) % len(uploaded_files)
        st.rerun()
    
    # Enhanced thumbnail gallery
    st.markdown("### 🖼️ Photo Gallery")
    
    # Create thumbnail grid
    num_cols = min(4, len(uploaded_files))
    cols = st.columns(num_cols)
    
    for i, uploaded_file in enumerate(uploaded_files):
        try:
            img = Image.open(uploaded_file)
            with cols[i % num_cols]:
                # Add glow effect to current image thumbnail
                button_style = "background: linear-gradient(45deg, #ff69b4, #ff1493); color: white;" if i == st.session_state.current_image else ""
                
                if st.button(f"📸 Photo {i+1}", key=f"thumb_{i}"):
                    st.session_state.current_image = i
                
                # Apply mini effects to thumbnails
                thumb_img = apply_image_effects(img, brightness*0.8, contrast*0.8, saturation*0.8)
                st.image(thumb_img, use_container_width=True)
                st.caption(f"✨ {uploaded_file.name}")
                
        except Exception as e:
            with cols[i % num_cols]:
                st.error(f"Error loading {uploaded_file.name}")
    
    # Enhanced final personalized message
    final_message = st.session_state.custom_message if st.session_state.custom_message else "Stay Happy Always! Wishing You Love, Luck and Light ✨"
    name_part = f" {st.session_state.birthday_name}" if st.session_state.birthday_name else ""
    
    st.markdown(f"""
    <div class="final-message">
        💖 {final_message}{name_part} 💖<br>
        <small>🎂 Hope this year brings you everything wonderful! 🌟</small><br>
        <small>✨ Created with love on {datetime.now().strftime('%B %d, %Y')} ✨</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced download option
    st.markdown("### 💾 Save Your Creation")
    if st.button("📥 Generate Enhanced Summary"):
        summary = f"""
        🎉 BIRTHDAY SLIDESHOW SUMMARY 🎉
        
        👤 Name: {st.session_state.birthday_name or 'Special Person'}
        📸 Total Photos: {len(uploaded_files)}
        💝 Message: {st.session_state.custom_message or 'Default birthday wishes'}
        🎵 Music: {'Yes' if uploaded_music else 'No'}
        ⚡ Auto-play: {'Enabled' if st.session_state.auto_advance else 'Disabled'}
        🎨 Effects: {'Applied' if st.session_state.image_effects else 'None'}
        ⏱️ Speed: {st.session_state.slideshow_speed} seconds
        📅 Created: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        
        Photos included:
        {chr(10).join([f"• {f.name}" for f in uploaded_files])}
        
        Beautiful quotes used:
        {chr(10).join([f"• {quote}" for quote in BEAUTIFUL_QUOTES[:len(uploaded_files)]])}
        
        ✨ Created with love and magic! ✨
        """
        st.download_button(
            label="💾 Download Enhanced Summary",
            data=summary,
            file_name=f"birthday_slideshow_{st.session_state.birthday_name or 'special'}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

else:
    # Enhanced welcome message
    st.markdown("""
    <div style="text-align: center; padding: 50px; 
                background: linear-gradient(135deg, #ffeef8, #fff0f8, #ffe4e6); 
                border-radius: 25px; margin: 20px 0; 
                border: 3px solid #ff69b4;
                animation: welcome-glow 3s ease-in-out infinite alternate;">
        <h2 style="color: #ff1493; animation: bounce 2s infinite;">🎈 Welcome to Birthday Gift Creator! 🎈</h2>
        <p style="font-size: 1.3em; color: #ff69b4;">Upload photos above to create a magical birthday slideshow</p>
        <p style="font-size: 1.1em; color: #ff1493;">✨ New Enhanced Features:</p>
        <div style="text-align: left; display: inline-block; background: rgba(255,255,255,0.7); 
                    padding: 20px; border-radius: 15px; margin: 20px;">
            <ul style="color: #c71585; font-size: 1.05em;">
                <li>🎵 Auto-play music during slideshow</li>
                <li>✨ Beautiful image effects and filters</li>
                <li>💫 Animated borders and sparkle effects</li>
                <li>📝 Inspirational quotes on each photo</li>
                <li>🎨 Customizable brightness, contrast, saturation</li>
                <li>⏱️ Adjustable slideshow speed</li>
                <li>🎼 Floating musical notes animation</li>
                <li>🌟 Enhanced visual transitions</li>
            </ul>
        </div>
        <p style="font-size: 1.2em; color: #ff69b4; margin-top: 20px;">
            🎂 Create memories that sparkle with magic! 🎂
        </p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p style="font-size: 2.5em; animation: rainbow 3s ease-in-out infinite;">
        🎂🎈🎁🌟💝🎉🎊✨🎵🎶
    </p>
    <p style="color: #ff69b4; font-size: 1.2em; font-weight: bold;">
        Made with ❤️ and ✨ for magical birthdays
    </p>
    <p style="color: #888; font-style: italic;">
        Creating beautiful memories, one slideshow at a time 🌟
    </p>
</div>
""", unsafe_allow_html=True)
