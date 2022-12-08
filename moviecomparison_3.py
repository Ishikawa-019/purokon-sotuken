import cv2
import matplotlib.pyplot as plt
import os
#from feat.tests.utils import get_test_data_path
from PIL import Image
from deepface import DeepFace
from feat import Detector
from feat import Fex
fex = Fex()
import glob
# rf: https://py-feat.org/content/intro.html#available-models

detector = Detector()

files = glob.glob(r'C:\Users\dishi\pro_con\moviedata\moviedata*.jpg')
print(files)
for image in files: 
    detector.detect_image(image, outputFname = image.replace(".jpg", ".csv"))