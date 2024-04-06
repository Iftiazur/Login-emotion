import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Load the trained model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])
model.load_weights('emotion_detection_model.h5')

# Define a function to detect and classify emotions
def detect_emotions(frame, emotion_counts):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using a face cascade classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) for the face
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48))
        roi_gray = np.reshape(roi_gray, (1, 48, 48, 1))

        # Make predictions using the model
        predicted_emotion = model.predict(roi_gray)
        emotion_label = np.argmax(predicted_emotion)

        # Define emotions
        emotions = ["Angry", "Disgusted", "Fearful", "Happy", "Neutral", "Sad", "Surprised"]
        emotion = emotions[emotion_label]
        emotion_counts[emotion] += 1

        # Draw a rectangle around the face and label the emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame

# Open a connection to the camera (you may need to adjust the camera index)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Create a window to display the output
cv2.namedWindow("Emotion Detection", cv2.WINDOW_NORMAL)

# Initialize the loop variables
emotion_counts = {emotion: 0 for emotion in ["Angry", "Disgusted", "Fearful", "Happy", "Neutral", "Sad", "Surprised"]}
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Detect emotions and display the result
    output_frame = detect_emotions(frame, emotion_counts)
    cv2.imshow("Emotion Detection", output_frame)

    # Break the loop if the 'ESC' key is pressed
    if cv2.waitKey(1) == 27:  # ASCII code for 'ESC'
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
