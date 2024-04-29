import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
# Define the valid username and password
valid_username = "user"
valid_password = "password"

# Page title
st.title("Login/Sign Up Page")

# Display the login form
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Check if the user clicked the "Login" button
if st.button("Login"):
    if username == valid_username and password == valid_password:
        st.success("Login successful!")
        st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)

    else:
        st.error("Invalid username or password. Please try again.")

# Display a sign-up form
st.write("Don't have an account? Sign up below.")
new_username = st.text_input("New Username")
new_password = st.text_input("New Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

# Check if the user clicked the "Sign Up" button
if st.button("Sign Up"):
    if new_password == confirm_password:
        valid_username = new_username
        valid_password = new_password
        st.success("Account created successfully! Please login.")
    else:
        st.error("Passwords do not match. Please try again.")