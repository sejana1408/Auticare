import streamlit as st
import random
import time

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
    st.page_link("pages/drawing.py",label="🖌️Drawing")

with st.sidebar.expander("Caretakers", expanded=False):
    st.page_link("pages/bot.py", label="🤖 Chat with the Bot")
    st.page_link("pages/test.py", label="🧩 M-CHAT Screening Test")
    st.page_link("pages/breathing.py",label="🧘 Breathing")
    st.page_link("pages/facial_app.py", label="👀 Facial emotion recognition")
# Clear session state on first run
if 'initialized' not in st.session_state:
    st.session_state.clear()
    st.session_state.initialized = True  # Prevents clearing on every rerun

# Define colors
color_names = {
    '#ff69b4': 'Pink',
    '#87ceeb': 'Sky Blue',
    '#90ee90': 'Light Green',
    '#ffff00': 'Yellow',
    '#800080': 'Purple'
}

# Define puzzles
puzzles = [
    {"sequence": ['#ff69b4', '#87ceeb', '', '#90ee90'], "correct": '#ffff00'},
    {"sequence": ['#800080', '', '#ff69b4', '#87ceeb'], "correct": '#90ee90'},
    {"sequence": ['#ffff00', '#90ee90', '', '#800080'], "correct": '#ff69b4'}
]

# Initialize session state variables
if 'current_puzzle' not in st.session_state:
    st.session_state.current_puzzle = 0
if 'shuffled_choices' not in st.session_state:
    st.session_state.shuffled_choices = []
if 'selected_color' not in st.session_state:
    st.session_state.selected_color = None
if 'correct_message' not in st.session_state:
    st.session_state.correct_message = None
if 'wrong_attempt' not in st.session_state:
    st.session_state.wrong_attempt = False  # Track wrong attempts only after a selection

def load_puzzle():
    puzzle = puzzles[st.session_state.current_puzzle]
    st.markdown("<h2 style='text-align: center;'>🎨 Color Pattern Game 🎤</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Find the Missing Color!</h4>", unsafe_allow_html=True)

    # Display the sequence
    cols = st.columns(len(puzzle['sequence']))
    for idx, color in enumerate(puzzle['sequence']):
        if color:
            cols[idx].markdown(f"""<div style='width: 80px; height: 80px; background-color: {color}; 
                                border: 3px solid black; border-radius: 10px;'></div>""", unsafe_allow_html=True)
        else:
            cols[idx].markdown(f"""<div style='width: 80px; height: 80px; background-color: white; 
                                border: 3px dashed black; border-radius: 10px;'></div>""", unsafe_allow_html=True)

    # Shuffle choices only if not set
    if not st.session_state.shuffled_choices:
        present_colors = [c for c in puzzle['sequence'] if c != '']
        choices = present_colors + [puzzle['correct']]
        random.shuffle(choices)
        st.session_state.shuffled_choices = choices

    st.write("### Choose the missing color:")

    # Create buttons with actual colors
    choice_cols = st.columns(len(st.session_state.shuffled_choices))
    for i, color in enumerate(st.session_state.shuffled_choices):
        button_html = f"""
        <button style="background-color: {color}; width: 100%; height: 80px; border: 3px solid black; 
        border-radius: 10px;" onclick="window.location.href='/?color={color}'">{color_names[color]}</button>
        """
        choice_cols[i].markdown(button_html, unsafe_allow_html=True)
        if choice_cols[i].button("", key=color, help=f"Click to select {color_names[color]}", use_container_width=True):
            check_answer(color)

    # Show correct message & move to next puzzle after 2s
    if st.session_state.correct_message:
        st.success(st.session_state.correct_message)
        time.sleep(2)
        next_puzzle()

    # Show error message **only after a wrong attempt**
    if st.session_state.wrong_attempt:
        st.error("Wrong! Try again 😢.")

def check_answer(selected_color):
    puzzle = puzzles[st.session_state.current_puzzle]
    correct_color = puzzle['correct']

    if selected_color == correct_color:
        color_name = color_names[correct_color]
        st.session_state.correct_message = f"🎉 Good job! You chose {color_name}!"
        st.balloons()
        st.session_state.selected_color = selected_color  # Set color only after selection
        st.session_state.wrong_attempt = False  # Reset wrong attempt flag
    else:
        st.session_state.correct_message = None
        st.session_state.wrong_attempt = True  # Set wrong attempt flag

def next_puzzle():
    # Move to the next puzzle and reset necessary variables
    st.session_state.current_puzzle = (st.session_state.current_puzzle + 1) % len(puzzles)
    st.session_state.shuffled_choices = []
    st.session_state.selected_color = None
    st.session_state.correct_message = None
    st.session_state.wrong_attempt = False
    st.rerun()

# Load the puzzle
load_puzzle()
