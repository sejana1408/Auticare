import streamlit as st
import time

st.set_page_config(page_title="Breathing Buddy", layout="centered")

st.markdown(
    """
    <style>
        /* Hide the default sidebar navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        .button {
            background-color: #FFDD57; /* Bright yellow */
            color: #000; /* Black text */
            border: none;
            border-radius: 10px;
            padding: 15px;
            font-size: 20px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .button:hover {
            background-color: #FFAB00; /* Darker yellow on hover */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for caretakers
st.sidebar.title("Navigation")
st.sidebar.page_link("app.py",label='🏡Home')
with st.sidebar.expander("Games",expanded=True):
    st.page_link("pages/color_app.py", label="🎨 Find the Color")
    st.page_link("pages/emo_matching.py", label="😁 Emotion Matching")
    st.page_link("pages/drawing.py",label="🖌️Drawing")

with st.sidebar.expander("Caretakers", expanded=False):
    st.page_link("pages/bot.py", label="🤖 Chat with the Bot")
    st.page_link("pages/test.py", label="🧩 M-CHAT Screening Test")
    st.page_link("pages/breathing.py",label="🧘 Breathing")
    st.page_link("pages/facial_app.py", label="👀 Facial emotion recognition")


st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        .button {
            background-color: #FFDD57; 
            color: #000; 
            border: none;
            border-radius: 10px;
            padding: 15px;
            font-size: 20px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .button:hover {
            background-color: #FFAB00; 
        }
        @keyframes breathe {
            0% {transform: scale(1);}
            50% {transform: scale(1.5);}
            100% {transform: scale(1);}
        }
        .breathing-circle {
            width: 150px;
            height: 150px;
            background-color:rgb(243, 224, 208);
            border-radius: 50%;
            animation: breathe 6s infinite ease-in-out;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: auto;
        }
        .breathing-text {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            margin-top: 20px;
            color: white;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for breathing control
if "breathing_active" not in st.session_state:
    st.session_state.breathing_active = False  # Default: animation is stopped

st.title("🧘 Breathing Buddy")
st.write("Follow the expanding and contracting circle to control your breathing.")

# Slider to adjust breathing speed
breathing_speed = st.slider("Adjust breathing speed (seconds per cycle)", 4, 10, 6)

# Start and Stop buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Breathing Cycle"):
        st.session_state.breathing_active = True
with col2:
    if st.button("Stop Breathing Cycle"):
        st.session_state.breathing_active = False

# Display the breathing animation only if it's active
if st.session_state.breathing_active:
    st.markdown('<div class="breathing-circle"></div>', unsafe_allow_html=True)
    
    breathing_text = st.empty()

    # Run breathing cycle while active
    while st.session_state.breathing_active:
        breathing_text.markdown('<div class="breathing-text">Inhale...</div>', unsafe_allow_html=True)
        time.sleep(breathing_speed / 2)  # Wait for half the cycle
        breathing_text.markdown('<div class="breathing-text">Exhale...</div>', unsafe_allow_html=True)
        time.sleep(breathing_speed / 2)  # Wait for the other half of the cycle
else:
    st.write("Breathing cycle stopped. Click 'Start Breathing Cycle' to begin again.")
