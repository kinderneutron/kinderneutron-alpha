import cv2
import numpy as np
import serial
import time

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getUnconnectedOutLayersNames()

# Open a connection to the webcam (you may need to change the index based on your system)
cap = cv2.VideoCapture(0)

# Open a serial connection to Arduino (adjust the port accordingly)
ser = serial.Serial('COM5', 9600, timeout=1)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    height, width, _ = frame.shape

    # Convert the frame to a blob
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Forward pass through the network
    detections = net.forward(layer_names)

    # Flag to check if a person is detected
    person_detected = False

    # Process the detections
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and class_id == 0:  # Class ID 0 represents a person in COCO dataset
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                w = int(obj[2] * width)
                h = int(obj[3] * height)

                # Draw a bounding box around the person
                x = int(center_x - w/2)
                y = int(center_y - h/2)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print("Person Detected! Acknowledgement: Present")
                person_detected = True

    # If a person is detected, send a signal to Arduino
    if person_detected:
        ser.write(b'1')  # Send '1' to Arduino
    else:
        ser.write(b'0')  # Send '0' to Arduino

    # Display the frame
    cv2.imshow('Human Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam, close the serial connection, and close all windows
cap.release()
ser.close()
cv2.destroyAllWindows()
