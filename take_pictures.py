import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0)

lower_color = np.array([0, 0, 0])
upper_color = np.array([200, 200, 200])


if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    rgb_frame = cv.cvtColor(frame, cv.COLOR_RGBA2RGB)
    mask = cv.inRange(rgb_frame, lower_color, upper_color)
    result = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('frame1', frame)
    cv.imshow('frame2', result)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

