import streamlit as st
import cv2
import numpy as np
import requests
import json

class_labels = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light",
                    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
                    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
                    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
                    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
                    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
                    "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard",
                    "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
                    "scissors", "teddy bear", "hair drier", "toothbrush"]

def detect_objects(image_path, desired_classes=None, confidence_threshold=0.2, nms_threshold=0.4):
    net = cv2.dnn.readNet("C:\\Users\\User\\Desktop\\SE_Project\\darknet\\yolov4.weights", "C:\\Users\\User\\Desktop\\SE_Project\\darknet\\yolov4.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    image = cv2.imread(image_path)
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)


    # Process detections
    boxes = []
    confidences = []
    class_ids = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold:
                center_x = int(detection[0] * image.shape[1])
                center_y = int(detection[1] * image.shape[0])
                w = int(detection[2] * image.shape[1])
                h = int(detection[3] * image.shape[0])
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)

    detections = []
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            class_label = class_labels[class_ids[i]]
            if desired_classes is None or class_label in desired_classes:
                confidence = confidences[i]
                detections.append((class_ids[i], confidence, (x, y, w, h)))

                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                label = f"{class_label}: {confidence:.2f}"
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    st.image(image, channels="BGR", caption="Detected Objects")
    object_list = []
    # Print the detected objects
    for idx, (class_id, confidence, bbox) in enumerate(detections, start=1):
        class_label = class_labels[class_id]
        object_list.append(class_label)
        st.write(f"Object {idx}: {class_label} (confidence: {confidence:.2f})")

    return detections,object_list

def updateDB(room,object_list):
    # print(room)
    # print(object_list)
    if('token' not in st.session_state):
        st.switch_page("Login.py")
    token=st.session_state.token
    headers={'authorization': token,'Content-Type': 'application/json'}
    url='http://localhost:5000/item/'
    body={'room':room, 'itemList':object_list}
    body_json= json.dumps(body)
    # print(body_json)
    response = requests.post(url=url,headers=headers,data=body_json)
    # print('Status Code:', response.status_code)
    # print('Response Body:', response.json())
    # return response 
    return response.status_code

def main():
    st.title("Object Detection App")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image_path = "uploaded_image.jpg"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.read())

        st.write("Image uploaded!")

        st.subheader("Detection Settings")
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.2)
        nms_threshold = st.slider("NMS Threshold", 0.0, 1.0, 0.4)
        desired_classes = st.text_input("Desired Classes (comma-separated, leave empty for all classes)")

        if desired_classes:
            desired_classes = [c.strip() for c in desired_classes.split(",")]
        else:
            desired_classes = class_labels
        st.write("Detecting objects...")
        detections,object_list = detect_objects(image_path, desired_classes, confidence_threshold, nms_threshold)
        st.write("Update Your Items")
        room = st.text_input("Room Name")
        if st.button("Update"):
            if room and len(object_list)>0:
                status = updateDB(room,object_list)
                if status == 200:
                    st.success('Items updated!')
                else:
                    st.error("Something went wrong!")
            elif len(object_list)<1:
                st.error('No objects to update!')
            else:
                st.error("You must enter a room!")
                


if __name__ == "__main__":
    main()
