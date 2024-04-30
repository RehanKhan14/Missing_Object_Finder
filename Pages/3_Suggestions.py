import streamlit as st

# Create an input field for the object name
object_name = st.text_input("Enter the object to be found:")

# Display the object name
st.write("Object to be found:", object_name)
