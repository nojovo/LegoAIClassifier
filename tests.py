from pathlib import Path
from process_pictures import edit_picture
import cv2 as cv

cap = cv.VideoCapture("rtsp://192.168.137.26:8554/cam")

while cap.isOpened():
    ret, frame = cap.read()
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', frame)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
