import logging
import numpy as np
import cv2 as cv
import cam

logging.basicConfig(level=logging.DEBUG)
logging.debug("Current os: " + cam.os_type)

cap = cam.capture()

lower_color = np.array([0, 0, 0])
upper_color = np.array([200, 200, 200])

logging.debug("Frame: ", cam.get_frame(cap))

while True:
    frame = cam.get_frame(cap)

    rgb_frame = cv.cvtColor(frame, cv.COLOR_RGBA2RGB)
    mask = cv.inRange(rgb_frame, lower_color, upper_color)
    result = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('frame1', frame)
    cv.imshow('frame2', result)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

