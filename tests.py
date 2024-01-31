import logging
from pathlib import Path
import numpy as np
import cv2 as cv

lower_color = 0
upper_color = 240
noise_size = 5
edge_size = 5

final_picture_size = 100

example_folder = "pictures/example/"

example_picture = cv.imread("pictures/example/0-test_picture.png")


def edit_picture(raw_picture):
    gray_frame = cv.cvtColor(raw_picture, cv.COLOR_RGB2GRAY)
    cv.imwrite(example_folder + "1-grey_image.png", gray_frame)

    # create mask
    mask = cv.inRange(gray_frame, lower_color, upper_color)
    cv.imwrite(example_folder + "2-mask.png", mask)

    # remove noise from mask
    kernel = np.ones((noise_size, noise_size), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    cv.imwrite(example_folder + "3-new_mask.png", mask)

    # find contours
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour_image = gray_frame.copy()
    contour_image = cv.drawContours(contour_image, contours, -1, (0, 255, 0), 3)
    cv.imwrite(example_folder + "4-contours.png", contour_image)

    # draw rectangle and crop image
    if len(contours) > 0:
        contour = contours[0]
        x, y, w, h = cv.boundingRect(contour)  # x and y are coordinates for top left corner
        center = (x + w / 2, y + h / 2)
        center_x, center_y = center

        # convert picture to a square by choosing the longer side as side length
        if w > h:
            h = w
        elif h > w:
            w = h

        # calculate new width, height and top left corner x and y
        w += edge_size * 2
        h += edge_size * 2
        new_x = round(center_x - w / 2)
        new_y = round(center_y - h / 2)

        # check if picture extract with edge can be cropped else return empty
        picture_height, picture_width = gray_frame.shape
        if new_x < 0:
            # new_x = 0
            return np.array([])
        if new_y < 0:
            # new_y = 0
            return np.array([])
        if new_x + w > picture_width:
            return np.array([])
        if new_y + h > picture_height:
            return np.array([])

        rectangle_image = gray_frame.copy()
        rectangle_image = cv.rectangle(rectangle_image, (new_x, new_y), (new_x + w, new_y + h), (0, 255, 0), 2)

        cropped_image = gray_frame[new_y:new_y + h, new_x:new_x + w]

        cv.imwrite(example_folder + "5-rectangle.png", rectangle_image)
        cv.imwrite(example_folder + "6-cropped.png", cropped_image)

        return cropped_image

    else:
        # return empty array if no part was found
        return np.array([])


new_image = edit_picture(example_picture)
