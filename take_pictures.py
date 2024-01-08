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

final_picture_size = 100

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
    # cv.imshow("mask", mask)

    # apply mask to image
    masked_image = cv.bitwise_and(frame, frame, mask=mask)
    # cv.imshow("masked", masked_image)

    # find contours
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour_image = gray_frame.copy()
    contour_image = cv.drawContours(contour_image, contours, -1, (0, 255, 0), 3)
    cv.imshow("contour", contour_image)

    # draw contours and crop image
    if len(contours) > 0:
        contour = contours[0]
        x, y, w, h = cv.boundingRect(contour)
        center = (x + w / 2, y + h / 2)
        center_x, center_y = center

        # convert picture to square by choosing the longer side as sie length
        if w > h:
            h = w
        elif h > w:
            w = h

        # calculate new width, height and top left corner x and y
        w += edge_size * 2
        h += edge_size * 2
        new_x = round(center_x - w / 2)
        new_y = round(center_y - h / 2)

        # check if picture extract with edge can be cropped else make it croppable
        picture_height, picture_width = gray_frame.shape
        if new_x < 0:
            new_x = 0
        if new_y < 0:
            new_y = 0
        if new_x + w > picture_width:
            w = picture_width - new_x
        if new_y + h > picture_height:
            w = picture_width - new_x

        rectangle_image = gray_frame.copy()
        rectangle_image = cv.rectangle(rectangle_image, (new_x, new_y), (new_x + w, new_y + h), (0, 255, 0), 2)

        cropped_image = gray_frame[new_y:new_y + h, new_x:new_x + w]

        cv.imshow("rectangle", rectangle_image)
        cv.imshow("cropped", cropped_image)

        # resize image
        new_image_dimensions = (final_picture_size, final_picture_size)
        resized_image = cv.resize(cropped_image, new_image_dimensions)
        cv.imshow("resized", resized_image)

        # save image
        cv.imwrite("old_image.png", cropped_image)
        cv.imwrite("new_image.png", resized_image)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

