import streamlit as st 
import ollama
import PyPDF2
import os 

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

def extract_pdf_text(uploaded_file):
    reader=PyPDF2.PdfReader(uploaded_file)
    text=''
    for page in reader.pages:
        text+=page.extract_text()+"\n"
    return text      

def get_llm_response(query,context):
    prompt=f'''
You are a Chat assistant placed in an application that helps the kids with autism and their caretakers. You are designed to help the caretakers. Therefore always be empathetic.


Answer the question based only on the context
If you dont know the answer, say I dont know

Context:
{context}

Question:{query}

Instructions:
Always be empathetic.
Answers must be concise and readable.
Provide words of affirmation and support.

Answer:
'''
    try:
        response=ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return{f'error:{e}'}

st.title("Auticare")
st.write("Your autism care helper")

uploaded_file=r'C:\Users\Sejana R\OneDrive\Desktop\auticare\auticare\autism_caregiving_data.pdf'

context=extract_pdf_text(uploaded_file)

query=st.chat_input("ask something")
messages=st.container(height=100)
messages.chat_message("assistant").write("Hello I am Auticare. A chat assistant designed to help you with your concerns on Autism") 


if query:
    messages=st.container(height=100)
    messages.chat_message("user").write(query)
    answer=get_llm_response(query,context)
    
    st.write(answer)
  
    if "test" in query.lower():
        st.info(" You can use the 'TEST' section in the application which uses M-CHAT for an initial screening")