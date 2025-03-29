import streamlit as st
import torch
import torch.nn as nn
import cv2
import numpy as np
from PIL import Image
from transformers import ViTFeatureExtractor, ViTModel

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

# Define the model class (same as training)
class ViTClassifier(nn.Module):
    def __init__(self, model_checkpoint, num_classes):
        super(ViTClassifier, self).__init__()
        self.vit = ViTModel.from_pretrained(model_checkpoint)
        self.classifier = nn.Linear(self.vit.config.hidden_size, num_classes)

    def forward(self, x):
        outputs = self.vit(pixel_values=x)
        logits = self.classifier(outputs.last_hidden_state[:, 0, :])
        return logits

# Load model and feature extractor
model_checkpoint = "google/vit-base-patch16-224-in21k"
image_processor = ViTFeatureExtractor.from_pretrained(model_checkpoint)
num_classes = 6  # Adjust based on your dataset
model_path = r'C:\Users\Sejana R\OneDrive\Desktop\auticare\auticare\best_model.pth'
model = ViTClassifier(model_checkpoint, num_classes)
model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
model.eval()

# Emotion labels (update based on your dataset)
emotions = ['Natural', 'Anger', 'Fear', 'Joy', 'Sadness', 'Surprise']

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Streamlit UI
st.title("Live Facial Emotion Detection")
st.write("Click 'Start Camera' to begin detecting emotions.")

# Initialize session state for camera
if "camera_active" not in st.session_state:
    st.session_state["camera_active"] = False

# Buttons to control camera
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Camera"):
        st.session_state["camera_active"] = True
with col2:
    if st.button("Stop Camera"):
        st.session_state["camera_active"] = False

# Start Webcam if activated
FRAME_WINDOW = st.image([])

cap = None  # Initialize camera variable

if st.session_state["camera_active"]:
    cap = cv2.VideoCapture(0)  # Start webcam

    while cap.isOpened() and st.session_state["camera_active"]:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image. Please check your webcam.")
            break

        # Convert OpenCV frame (BGR) to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = image_rgb[y:y+h, x:x+w]  # Extract face region

            # Convert face region to PIL Image
            face_pil = Image.fromarray(face_roi)

            # Preprocess image
            image_encodings = image_processor(face_pil, return_tensors="pt")
            pixel_values = image_encodings['pixel_values']

            # Predict emotion
            with torch.no_grad():
                logits = model(pixel_values)
                prediction = torch.argmax(logits, dim=1).item()
                emotion_text = emotions[prediction]

            # Draw bounding box and emotion label
            cv2.rectangle(image_rgb, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image_rgb, emotion_text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
            

           
            audio_placeholder = st.empty()
            calming_sound_path=r'C:\Users\Sejana R\OneDrive\Desktop\auticare\smand__nightingale-song(chosic.com).mp3'
            # Initialize session state to track last played emotion
            if "last_played_emotion" not in st.session_state:
                st.session_state["last_played_emotion"] = None


            # Play sound only if emotion has changed
            if emotion_text in ["Sadness"] and st.session_state["last_played_emotion"] != emotion_text:
                st.session_state["last_played_emotion"] = emotion_text  # Update session state
                audio_placeholder.empty()  # Clear previous audio before playing
                audio_placeholder.audio(calming_sound_path, format="audio/mp3")  # Play new audio

            # Reset flag when emotion is "Natural"
            elif emotion_text == "Natural":
                st.session_state["last_played_emotion"] = None
        # Show frame in Streamlit
        FRAME_WINDOW.image(image_rgb, channels="RGB")

    cap.release()
    cv2.destroyAllWindows()
else:
    st.write("Camera is stopped.") 
