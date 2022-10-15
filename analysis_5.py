from feat import Detector

detector = Detector(
    face_model     = "retinaface",
    landmark_model = "mobilefacenet",
    au_model       = 'svm',
    emotion_model  = "resmasknet",
    facepose_model = "img2pose",
)
detector

import glob
import cv2
import matplotlib.pyplot as plt
import os
from PIL import Image

for images in glob.glob("./imagedata/*.jpg"):
    img = cv2.imread(images[n])
    image_prediction = detector.detect_image(img)
    image_prediction
    image_prediction.plot_face()
