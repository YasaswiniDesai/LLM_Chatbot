import streamlit as st

# Sample user credentials for login
users = {
    'admin': 'password123'  # Example username and password
}

# Function to authenticate the user
def authenticate(username, password):
    return username in users and users[username] == password

# Streamlit app for login
st.title("Streamlit Login Example")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Display the appropriate page based on login status
if st.session_state.logged_in:
    main_application()  # Calls the function from new.py
else:
    st.header("Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login successful! Redirecting...")
            st.session_state.logged_in = True
            # No rerun needed; the page will automatically display main_application on next interaction
        else:
            st.error("Invalid username or password.")

