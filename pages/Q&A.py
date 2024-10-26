import os
import streamlit as st
import requests
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Set Streamlit page configuration at the very beginning
st.set_page_config(page_title="Gemini Image Demo")

load_dotenv()

# Set up Google API for generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS for input field, file uploader, and buttons
st.markdown("""
    <style>
    /* Input text field */
    .stTextInput > div > div > input {
        background-color: black;
        color: white;
    }

    /* File uploader styling */
    .stFileUploader > div > div {
        background-color: black;
        color: white;
    }

    /* Style for the 'Browse files' button inside file uploader */
    .stFileUploader > label > div {
        background-color: white;
        color: black;
    }

    /* Style the button background and text */
    .stButton > button {
        background-color: black;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.header("Image Analysis")

# Input prompt styling
input=st.text_input("Input Prompt: ",key="input")

# File uploader for image input
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "pdf"])

# Display uploaded image if available
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button for processing
submit=st.button("Tell me about the image")

# Function to load Google Gemini model and get response
def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,image[0],prompt])
    return response.text

# Function to prepare image data for processing
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Prompt for analyzing the image (e.g., an invoice)
input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image.
               """

# If the submit button is clicked
if submit and uploaded_file:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    
    # Display the model's response
    st.subheader("The Response is")
    st.write(response)
