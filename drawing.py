import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import numpy as np
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

emotions = ["Happy", "Sad", "Angry", "Surprised", "Excited", "Fearful"]


st.title("Emotion Drawing Game 🎨")
st.subheader("Draw the emotion shown below!")


if "current_emotion" not in st.session_state:
    st.session_state.current_emotion = random.choice(emotions)

st.write(f"Draw: {st.session_state.current_emotion}")


if "canvas_data" not in st.session_state:
    st.session_state.canvas_data = None


canvas_result = st_canvas(
    fill_color="rgba(255,255,255,0)",  
    stroke_width=5,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=300,
    width=300,
    drawing_mode="freedraw",
    key="canvas"
)


if canvas_result.image_data is not None:
    st.session_state.canvas_data = canvas_result.image_data


if st.session_state.canvas_data is not None:
    
    image = Image.fromarray((st.session_state.canvas_data[:, :, :3] * 255).astype(np.uint8))

 
    if st.button("Save Drawing"):
       
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        
        st.download_button(
            label="Download Image",
            data=buffer,
            file_name="drawing.png",
            mime="image/png"
        )


if st.button("New Emotion"):
    
    st.session_state.canvas_data = None
   
    st.session_state.current_emotion = random.choice(emotions)
    
    st.rerun()
