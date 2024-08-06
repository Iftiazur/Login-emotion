# Face Recognition and Emotion Detection System

This project is a comprehensive Face Recognition and Emotion Detection system implemented in Python. It provides a graphical user interface for user registration, login, and emotion detection using facial recognition technology.

## Features

- User registration with facial data capture
- Face recognition-based login system
- Real-time emotion detection
- User session tracking
- Emotion frequency visualization

## Components

1. **Main Application (app-gui.py)**
   - Implements the graphical user interface using tkinter
   - Manages different pages for registration, login, and user sessions
   - Integrates face recognition and emotion detection functionalities

2. **Classifier Creation (create_classifier.py)**
   - Trains a Local Binary Patterns Histograms (LBPH) face recognizer
   - Creates classifier XML files for registered users

3. **Dataset Creation (create_dataset.py)**
   - Captures facial images for new user registration
   - Implements a progress meter for image capture

4. **Face Detection and Recognition (Detector.py)**
   - Performs real-time face detection and recognition
   - Verifies user identity for login

5. **Emotion Detection (emotion_detection.py)**
   - Utilizes a pre-trained convolutional neural network for emotion classification
   - Detects and displays emotions in real-time video feed

6. **Emotion Detection Testing (testerFile.py)**
   - Provides a testing interface for the emotion detection system
   - Allows real-time emotion detection and frequency visualization

7. **Emotion Detection Model Training (training.py)**
   - Defines and trains a convolutional neural network for emotion detection
   - Uses image data generators for efficient training
   - Saves the trained model weights

## Requirements

- Python 3.x
- OpenCV
- TensorFlow
- Tkinter
- Matplotlib
- NumPy

