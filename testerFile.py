import cv2
import matplotlib.pyplot as plt
import emotion_detection  # Import your emotion detection module

def testingEmotionDetection():
    emotion_counts = {emotion: 0 for emotion in
                      ["Angry", "Disgusted", "Fearful", "Happy", "Neutral", "Sad", "Surprised"]}
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_with_emotions = emotion_detection.detect_emotions(frame, emotion_counts)

        cv2.imshow('Emotion Detection', frame_with_emotions)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('b'):
            # Create a bar chart to display the emotion frequencies
            plt.bar(emotion_counts.keys(), emotion_counts.values())
            plt.xlabel("Emotion")
            plt.ylabel("Frequency")
            plt.title("Emotion Frequency Graph")
            plt.show()
        elif key & 0xFF == ord('q'):  # Press 'b' to terminate the program
            break

testingEmotionDetection()