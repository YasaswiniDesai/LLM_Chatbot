import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Set up Google API for generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit app configuration
st.set_page_config(page_title="URL Analysis for Fake News Detection")

st.header("Fake News Detector")

# Custom CSS to style the input field
st.markdown("""
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: black;
        color: white;
        border: 1px solid #ccc;
    }
    .stButton > button {
        background-color: #444;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Input for URL
url_input = st.text_input("Enter a URL to analyze: ", key="url_input")

# Button to submit URL for analysis
submit = st.button("Analyze URL")

# Function to fetch webpage content
def fetch_url_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            st.error(f"Error: Unable to fetch content. HTTP Status Code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Function to analyze content using the LLM
def analyze_content(content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([content, prompt])
    return response.text

# Prompt for fake news detection
fake_news_prompt = """
You are a highly specialized expert in fake news detection, leveraging an extensive database of verified facts, trusted fact-checking sources, and sophisticated linguistic analysis to detect misinformation.
Thoroughly analyze the following content and classify it as either true, false, half-truth, political propaganda, or misleading. Cross-reference with trusted databases to identify any inconsistencies, manipulative language, or unreliable claims.
Provide a short, clear verdict and a concise explanation of your findings, citing specific reasons and evidence. 
Conclude with a definitive, well-supported assessment.
"""

# If submit button is clicked
if submit and url_input:
    # Fetch the content of the URL
    webpage_content = fetch_url_content(url_input)
    
    if webpage_content:
        # Use BeautifulSoup to parse the HTML and extract meaningful text
        soup = BeautifulSoup(webpage_content, 'html.parser')
        text_content = soup.get_text(separator=" ", strip=True)  # Extract all the text

        # Limit text content to a manageable size
        text_content = text_content[:3000]  # Let's limit to the first 3000 characters

        # Analyze the content for fake news
        response = analyze_content(text_content, fake_news_prompt)
        
        # Display the response from the model
        st.subheader("The Analysis Result:")
        st.write(response)
