import logging
import numpy as np
import cv2 as cv
import cam

logging.basicConfig(level=logging.DEBUG)
logging.debug("Current os: " + cam.os_type)

lower_color = 250
upper_color = 255
connectivity = 4

cap = cam.capture()


while True:
    frame = cam.get_frame(cap)
    gray_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

    mask = cv.inRange(gray_frame, lower_color, upper_color)

    # remove noise from mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)

    masked_image = cv.bitwise_and(frame, frame, mask=mask)

    # find contours
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour_im = gray_frame
    contour_im = cv.drawContours(contour_im, contours, -1, (0, 255, 0), 3)

    # draw contours and crop image
    if len(contours) > 0:
        contour = contours[0]
        x, y, w, h = cv.boundingRect(contour)
        rect_im = gray_frame
        rect_im = cv.rectangle(rect_im, (x, y), (x + w, y + h), (0, 255, 0), 2)

        crop_img = gray_frame[y:y + h, x:x + w]

    # cv.imshow("raw_image", frame)
    cv.imshow("grey_image", gray_frame)
    cv.imshow("mask", mask)
    # cv.imshow("masked_image", masked_image)
    cv.imshow("contour_im", contour_im)
    cv.imshow("rect_im", rect_im)
    cv.imshow("crop_img", crop_img)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

