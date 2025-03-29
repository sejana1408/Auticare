import streamlit as st 

# Set page configuration
st.set_page_config(page_title="Autistic Kids Helper", page_icon=":sparkles:", layout="wide")

# Hide the default sidebar navigation
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
    st.page_link("pages/drawing.py",label="🖌️ Drawing")

with st.sidebar.expander("Caretakers", expanded=False):
    st.page_link("pages/bot.py", label="🤖 Chat with the Bot")
    st.page_link("pages/test.py", label="🧩 M-CHAT Screening Test")
    st.page_link("pages/breathing.py",label="🧘 Breathing")
    st.page_link("pages/facial_app.py", label="👀 Facial emotion recognition")

# Main page content
with st.container(height=250):
    st.markdown(
        """
        <div style="text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <h1 style="color: #FF6F61;">👋 Hello! I am Auticare!</h1>
            <h2 style="color: #6B5B95;">Your Personal Healthcare Companion.</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# Games section
st.markdown("## 🎮 Let's Play Some Games!")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    #if st.button("🎨 Guess the Color", key="color_game", help="Click to play!"):
        st.page_link("pages/color_app.py",label="🎨 Guess the Color")

with col2:
    #if st.button("😃 Match the Emotions", key="emotion_game", help="Click to play!"):
        st.page_link("pages/emo_matching.py",label="😃 Match the Emotions")

with col3:
    #if st.button("👀 Facial Emotion Recognition", key="facial_recognition", help="Click to play!"):
        st.page_link("pages/facial_app.py",label="👀 Facial Emotion Recognition")

with col4:
    #if st.button("🖌️ Drawing Fun", key="drawing_game", help="Click to play!"):
        st.page_link("pages/drawing.py",label="🖌️ Drawing Fun")

# Add a footer with a friendly message
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <h3 style="color: #6B5B95;">🌈 Have Fun and Learn!</h3>
        <p style="color: #FF6F61;">Remember, it's all about having fun while learning!</p>
    </div>
    """,
    unsafe_allow_html=True
)