import logging
import numpy as np
import cv2 as cv
import cam

logging.basicConfig(level=logging.DEBUG)
logging.debug("Current os: " + cam.os_type)

cap = cam.capture()

lower_color = 250
upper_color = 255

while True:
    frame = cam.get_frame(cap)

    grey_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    mask = cv.inRange(grey_frame, lower_color, upper_color)
    masked_image = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('raw_image', frame)
    cv.imshow("grey_image", grey_frame)
    cv.imshow('masked image', masked_image)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

