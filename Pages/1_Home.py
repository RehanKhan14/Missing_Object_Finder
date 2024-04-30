import streamlit as st
from streamlit_extras.switch_page_button import switch_page
def example():
    switch_to_next = st.button("Detect Objects")
    if switch_to_next:
        switch_page("Detection")
def example2():
    switch_to_next = st.button("Suggest Location")
    if switch_to_next:
        switch_page("Suggestions")
def main():
    st.title("Welcome to the Missing Object Detector")
    st.write(
        "In this application, we utilize the YOLO (You Only Look Once) model for object detection. Users can upload an image containing a room scene, and the detector will identify missing objects in the scene. Additionally, based on the data extracted from previously uploaded images, the application suggests objects that are commonly found in similar scenes but might be missing in the current one. This feature aims to enhance the user experience by providing helpful suggestions for completing the room's setup."
    )

    # st.image("images/yolo_example.jpg", caption="Example of Object Detection with YOLO", use_column_width=True)

    st.write("Click the buttons below to detect objects in an image or to suggest places to look for that image.")
    example()
    example2()


if __name__ == "__main__":
    main()

