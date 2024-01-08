import logging
import numpy as np
import cv2 as cv
import cam

logging.basicConfig(level=logging.DEBUG)
logging.debug("Current os: " + cam.os_type)

lower_color = 0
upper_color = 240
noise_size = 5
edge_size = 5

final_picture_size = 50

cap = cam.capture()


while True:
    # frame = cam.get_frame(cap)
    frame = cv.imread("test_image.png")
    # cv.imshow("raw_image", frame)

    gray_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    cv.imshow("grey_image", gray_frame)

    mask = cv.inRange(gray_frame, lower_color, upper_color)
    cv.imshow("mask", mask)

    # remove noise from mask
    kernel = np.ones((noise_size, noise_size), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    # cv.imshow("new_mask", mask)

    # apply mask to image
    masked_image = cv.bitwise_and(frame, frame, mask=mask)
    # cv.imshow("masked_image", masked_image)

    # find contours
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour_im = gray_frame.copy()
    contour_im = cv.drawContours(contour_im, contours, -1, (0, 255, 0), 3)
    cv.imshow("contour_im", contour_im)

    # draw contours and crop image
    if len(contours) > 0:
        contour = contours[0]
        x, y, w, h = cv.boundingRect(contour)
        center = (x + (w / 2), y + (h / 2))
        center_x, center_y = center
        w += edge_size * 2
        h += edge_size * 2
        new_x = round(center_x - (w / 2))
        new_y = round(center_y - (h / 2))

        rect_im = gray_frame.copy()
        rect_im = cv.rectangle(rect_im, (new_x, new_y), (new_x + w, new_y + h), (0, 255, 0), 2)

        crop_img = gray_frame[new_y:new_y + h, new_x:new_x + w]

    cv.imshow("rect_im", rect_im)
    cv.imshow("crop_img", crop_img)

    # resize image
    # new_image = cv.resize(crop_img)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

