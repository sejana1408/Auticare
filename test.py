import streamlit as st
import time
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

def test():

    # Title of the application
    st.title("Modified Checklist For Autism in Toddlers")
    @st.dialog("Information")
    def info():
        st.write("This screening test is for toddlers between the months of 16 and 30 to detect autism signs.It consists of 20 questions.")
        check=st.checkbox("I understand")
        if check:
            st.session_state['dialog_closed']=True
            time.sleep(0.5)
            st.rerun()
    if 'dialog_closed' in st.session_state and st.session_state['dialog_closed']:
        pass
    else:
        info()
    # Introduction
    st.write("This questionnaire is designed to help identify children who may be at risk for autism spectrum disorder (ASD). Please answer the following questions.")
    st.info("This is just a questionnaire. Do not conclude anything based on this diagnosis. Always consult a doctor.",icon="⚠️")
    # Questions
    questions = [
        "If you point at something across the room, does your child look at it?",
        "Have you ever wondered if your child might be deaf?",
        "Does your child play pretend or make-believe?",
        "Does your child like climbing on things?",
        "Does your child make unusual finger movements near his or her eyes?",
        "Does your child point with one finger to ask for something or to get help?",
        "Does your child point with one finger to show you something interesting?",
        "Is your child interested in other children?",
        "Does your child show you things by bringing them to you or holding them up for you to see - not to get help, but just to share?",
        "Does your child respond when you call his or her name?",
        "When you smile at your child, does he or she smile back at you?",
        "Does your child get upset by everyday noises?",
        "Does your child walk?",
        "Does your child look you in the eye when you are talking to him or her, playing with him or her, or dressing him or her?",
        "Does your child try to copy what you do?",
        "If you turn your head to look at something, does your child look around to see what you are looking at?",
        "Does your child try to get you to watch him or her?",
        "Does your child understand when you tell him or her to do something?",
        "If something new happens, does your child look at your face to see how you feel about it?",
        "Does your child like movement activities?"
    ]

    # Initialize session state
    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = [None] * len(questions)
    if 'show_warning' not in st.session_state:
        st.session_state.show_warning = False  # Track if a warning popup is needed

    # Function to reset quiz
    def reset_quiz():
        st.session_state.question_index = 0
        st.session_state.responses = [None] * len(questions)
        st.session_state.show_warning = False  # Reset warning

    # Display the current question
    if st.session_state.question_index < len(questions):
        with st.container(height=250, border=True):
            question = questions[st.session_state.question_index]

            # Retrieve saved response if available
            current_answer = st.session_state.responses[st.session_state.question_index]

            # Display radio button (without default selection)
            response = st.radio(
                question, ["Yes", "No"],
                index=None if current_answer is None else ["Yes", "No"].index(current_answer),
                
            )

            # Save the response
            if response:
                st.session_state.responses[st.session_state.question_index] = response

            st.write(f"You have answered {st.session_state.question_index + 1}/{len(questions)} questions")

            # Next button with validation
            if st.button("Next"):
                if st.session_state.responses[st.session_state.question_index] is None:
                    st.session_state.show_warning = True  # Show warning popup
                else:
                    st.session_state.show_warning = False  # Clear warning
                    st.session_state.question_index += 1  # Move to next question

            # Warning popup if no answer is selected
            if st.session_state.show_warning:
                @st.dialog("Warning")
                def show_warning():
                    st.write("⚠️ Please select an answer before proceeding!")

                show_warning()

    # Evaluate the results
    if st.session_state.question_index == len(questions):
        st.success("All Questions Answered")

        # Display responses
        st.write("### Your Responses:")
        for i in range(len(questions)):
            st.write(f"**Q{i + 1}:** {questions[i]}")
            st.write(f"**Answer:** {st.session_state.responses[i]}")

        # Scoring logic
        score = 0
        scoring_criteria = [
            ("No", 1), ("Yes", 0), ("No", 1), ("Yes", 1), ("Yes", 1),
            ("No", 1), ("No", 1), ("No", 1), ("No", 1), ("No", 1),
            ("No", 1), ("Yes", 1), ("No", 1), ("Yes", 0),
            ("No", 1), ("No", 1), ("No", 1), ("No", 1), ("No", 1)
        ]

        for i, (expected_answer, points) in enumerate(scoring_criteria):
            if st.session_state.responses[i] == expected_answer:
                score += points

        # Display the risk score
        @st.dialog("Assessment Score")
        def get_score():
            st.write(f"Your risk score is: **{score}**")
            if score >= 3:
                st.write("The results suggest that the child may be at risk for autism spectrum disorder (ASD).")
            else:
                st.write("The results suggest that the child is not at risk for autism spectrum disorder (ASD).")

        if st.button("Get Final Evaluation Results"):
            get_score()

    # Reset button
    if st.button("Start Over"):
        reset_quiz()

test()
