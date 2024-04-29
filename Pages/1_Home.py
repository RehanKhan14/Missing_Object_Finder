import streamlit as st
from streamlit_extras.switch_page_button import switch_page
def example():
    switch_to_next = st.button("Detect Objects")
    if switch_to_next:
        switch_page("Test")
def main():
    st.title("Welcome to the Missing Object Detector")
    st.write(
        "This application uses the YOLO (You Only Look Once) model for object detection. "
        "Upload an image and let the detector find missing objects in the scene."
    )

    # st.image("images/yolo_example.jpg", caption="Example of Object Detection with YOLO", use_column_width=True)

    st.write("Click the button below to detect objects in an image.")
    example()


if __name__ == "__main__":
    main()

