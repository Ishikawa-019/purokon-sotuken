import os
import datetime
import time
import cv2
import schedule

start = time.time()

camera = 0
capture = cv2.VideoCapture(camera)

def cut():
    ret, frame = capture.read()
    elapsed = time.time()
    dif = int(elapsed) - int(start)
    fname = "image_" + str(dif) + ".jpg"
    cv2.imwrite('imagedata/' + fname, frame)

schedule.every(1).seconds.do(cut)

while True:
  schedule.run_pending()
  time.sleep(1)
