import cv2

def main_app(name):
    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(f"./data/classifiers/{name}_classifier.xml")

    cap = cv2.VideoCapture(0)
    recognized_name = None

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            id, confidence = recognizer.predict(roi_gray)
            confidence = 100 - int(confidence)
            if confidence > 50:
                recognized_name = name.upper()
                text = f"Face verified: {recognized_name}. Press Enter to login."
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.7
                font_color = (0, 255, 0)  # Green color
                font_thickness = 2
                text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
                text_x = int((frame.shape[1] - text_size[0]) / 2)
                text_y = int(frame.shape[0] - 20)
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

                # Draw a rectangle around the recognized face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, recognized_name, (x, y - 10), font, font_scale, font_color, font_thickness)

        # Show progress meter
        if recognized_name:
            progress_text = "Recognized: " + recognized_name
        else:
            progress_text = "No recognition yet"
        cv2.putText(frame, progress_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Face Recognition", frame)
        key = cv2.waitKey(1)

        if recognized_name:
            if key == 13:  # Enter key
                cap.release()
                cv2.destroyAllWindows()
                return recognized_name
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return None

        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None

    cap.release()
    cv2.destroyAllWindows()
    return None
