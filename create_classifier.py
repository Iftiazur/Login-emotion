import cv2
import numpy as np
import os

def train_classifier(name):
    path = os.path.join(os.getcwd() + "/data/imageFiles/" + name + "/")
    faces = []
    ids = []

    for root, dirs, files in os.walk(path):
        for pic in files:
            img_path = os.path.join(path, pic)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Load image in grayscale
            image_np = np.array(img, 'uint8')
            id = int(pic.split('_')[0])  # Extract the image ID from the filename
            faces.append(image_np)
            ids.append(id)

    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write(f"./data/classifiers/{name}_classifier.xml")
