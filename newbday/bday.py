import streamlit as st
import base64
from PIL import Image
import time

st.set_page_config(page_title="🎉 Birthday Gift Creator", layout="centered")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #ff69b4;
        font-size: 3em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
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
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 10px #ff69b4; }
        to { box-shadow: 0 0 20px #ff69b4, 0 0 30px #ff69b4; }
    }
    
    .slideshow-container {
        position: relative;
        margin: 20px 0;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .upload-section {
        background: linear-gradient(45deg, #f0f8ff, #e6f3ff);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border: 2px dashed #4169e1;
    }
    
    .control-buttons {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin: 20px 0;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #ff69b4, #ff1493);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 105, 180, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_image' not in st.session_state:
    st.session_state.current_image = 0
if 'auto_advance' not in st.session_state:
    st.session_state.auto_advance = False
if 'birthday_name' not in st.session_state:
    st.session_state.birthday_name = ""
if 'custom_message' not in st.session_state:
    st.session_state.custom_message = ""

# Header Section
st.markdown('<h1 class="main-title">🎉 Birthday Gift Creator 🎉</h1>', unsafe_allow_html=True)

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

# Background Music
if uploaded_music:
    try:
        audio_bytes = uploaded_music.read()
        b64 = base64.b64encode(audio_bytes).decode()
        md = f"""
        <audio autoplay loop controls style="width: 100%; margin: 20px 0;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        Your browser does not support the audio element.
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)
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
            import random
            st.session_state.current_image = random.randint(0, len(uploaded_files) - 1)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display current image
    try:
        current_file = uploaded_files[st.session_state.current_image]
        img = Image.open(current_file)
        
        # Display image with container styling
        st.markdown('<div class="slideshow-container">', unsafe_allow_html=True)
        st.image(img, use_container_width=True, caption=f"Memory {st.session_state.current_image + 1} of {len(uploaded_files)} 📸")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Progress bar
        progress = (st.session_state.current_image + 1) / len(uploaded_files)
        st.progress(progress)
        
        # Image details
        st.markdown(f"**📁 File:** {current_file.name}")
        st.markdown(f"**📏 Size:** {img.size[0]} x {img.size[1]} pixels")
        
    except Exception as e:
        st.error(f"Error loading image: {e}")
    
    # Auto-advance functionality
    if st.session_state.auto_advance:
        time.sleep(3)  # Wait 3 seconds
        st.session_state.current_image = (st.session_state.current_image + 1) % len(uploaded_files)
        st.rerun()
    
    # Thumbnail gallery
    st.markdown("### 🖼️ Photo Gallery")
    
    # Create thumbnail grid
    num_cols = min(4, len(uploaded_files))
    cols = st.columns(num_cols)
    
    for i, uploaded_file in enumerate(uploaded_files):
        try:
            img = Image.open(uploaded_file)
            with cols[i % num_cols]:
                if st.button(f"📸 Photo {i+1}", key=f"thumb_{i}"):
                    st.session_state.current_image = i
                st.image(img, use_container_width=True)
                st.caption(f"{uploaded_file.name}")
        except Exception as e:
            with cols[i % num_cols]:
                st.error(f"Error loading {uploaded_file.name}")
    
    # Final personalized message
    final_message = st.session_state.custom_message if st.session_state.custom_message else "Stay Happy Always! Wishing You Love, Luck and Light ✨"
    name_part = f" {st.session_state.birthday_name}" if st.session_state.birthday_name else ""
    
    st.markdown(f"""
    <div class="final-message">
        💖 {final_message}{name_part} 💖<br>
        <small>🎂 Hope this year brings you everything wonderful! 🌟</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Download option
    st.markdown("### 💾 Save Your Creation")
    if st.button("📥 Generate Summary"):
        summary = f"""
        🎉 BIRTHDAY SLIDESHOW SUMMARY 🎉
        
        👤 Name: {st.session_state.birthday_name or 'Special Person'}
        📸 Total Photos: {len(uploaded_files)}
        💝 Message: {st.session_state.custom_message or 'Default birthday wishes'}
        🎵 Music: {'Yes' if uploaded_music else 'No'}
        
        Photos included:
        {chr(10).join([f"• {f.name}" for f in uploaded_files])}
        
        Created with love! 💕
        """
        st.download_button(
            label="💾 Download Summary",
            data=summary,
            file_name=f"birthday_slideshow_{st.session_state.birthday_name or 'special'}.txt",
            mime="text/plain"
        )

else:
    # Welcome message when no files uploaded
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: linear-gradient(45deg, #ffeef8, #fff0f8); border-radius: 15px; margin: 20px 0;">
        <h2>🎈 Welcome to Birthday Gift Creator! 🎈</h2>
        <p style="font-size: 1.2em;">Upload photos above to create a beautiful birthday slideshow</p>
        <p>✨ Features:</p>
        <ul style="text-align: left; display: inline-block;">
            <li>🎵 Add background music</li>
            <li>📸 Interactive photo slideshow</li>
            <li>🎨 Beautiful animations</li>
            <li>💝 Personalized messages</li>
            <li>🎲 Random photo selection</li>
            <li>📥 Download summary</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 2em;'>🎂🎈🎁🌟💝🎉🎊✨</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Made with ❤️ for special birthdays</p>", unsafe_allow_html=True)
