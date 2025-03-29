import streamlit as st
import random

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

# Emotion dictionary with image paths (replace with actual images)
emotions = {
    "Happy": r"C:\Users\Sejana R\OneDrive\Desktop\auticare\happy.png",
    "Sad": r"C:\Users\Sejana R\OneDrive\Desktop\auticare\sad.png",
    "Angry": r"C:\Users\Sejana R\OneDrive\Desktop\auticare\angry.png",
    "Surprised": r"C:\Users\Sejana R\OneDrive\Desktop\auticare\surprised.png"
}

# Function to reset the game
def reset_game():
    st.session_state.correct_emotion, st.session_state.image_path = random.choice(list(emotions.items()))
    st.session_state.options = random.sample(list(emotions.keys()), len(emotions))  # Shuffle options
    st.session_state.user_guess = None
    st.rerun()

# Initialize session state variables if not already set
if 'correct_emotion' not in st.session_state:
    
    reset_game()

# Streamlit UI
st.title("🎭 Emotion Detection Game")
st.write("Guess the correct emotion from the image below!")

# Display the image 
st.image(st.session_state.image_path, caption="What emotion is this?", use_container_width=True)

# User input (shuffled options)
st.session_state.user_guess = st.radio("Choose an emotion:", st.session_state.options)

# Display the user's guess
if st.session_state.user_guess:
    st.write(f"You selected: **{st.session_state.user_guess}**")

# Submit button
if st.button("Submit Guess"):
    if st.session_state.user_guess == st.session_state.correct_emotion:
        st.success("🎉 Correct! Well done!")
        st.balloons()
    else:
        st.error(f"❌ Oops! The correct answer was **{st.session_state.correct_emotion}**.")

# Option to play again (resets everything)
if st.button("Play Again"):
    reset_game()
