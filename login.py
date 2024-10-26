import streamlit as st

# Set the page configuration
st.set_page_config(page_title="Login Page", layout="centered")

# Inject CSS for background and text colors
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stTextInput > div > div > input {
        color: white;
        background-color: #333333;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
    }
    .stTitle {
        color: white;
    }
    .stSidebar {
        background-color: #fff!;
        color: white!;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Hardcoded username and password (for demonstration purposes)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# Initialize session state to track login status
if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False

# Function to handle login
def login(username, password):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        st.session_state['login_status'] = True
        st.success("Logged in successfully!")
    else:
        st.error("Invalid username or password.")

# Function to display the login page
def display_login_page():
    st.title("Login Page")
    
    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Login button
    if st.button("Login"):
        login(username, password)

# Function to display the main content after login
def display_main_content():
    st.title("Welcome to the Application")
    st.write("You have successfully logged in.")
    
    # Option to logout
    if st.button("Logout"):
        st.session_state['login_status'] = False
        st.experimental_rerun()

# Main logic
if not st.session_state['login_status']:
    display_login_page()
else:
    display_main_content()

st.sidebar.success("Select a page above.")
