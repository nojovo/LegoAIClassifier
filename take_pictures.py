import logging
import time
from pathlib import Path
import numpy as np
import cv2 as cv
import cam

logging.basicConfig(level=logging.DEBUG)
logging.debug("Current os: " + cam.os_type)

parts = ["32316", "32524", "32140", "32526", "64179", "32270", "32269", "2780", "32556", "32073"]

part_number = parts[0]
current_id = 1
number_of_pictures = 10
time_between_pictures = 0.01  # in seconds
save_raw_pictures = False
save_processed_pictures = False

lower_color = 0
upper_color = 180
noise_size = 5
edge_size = 5

final_picture_size = 100

cap = cam.capture()

raw_pictures_path = f"./pictures/raw/{part_number}"
processed_pictures_path = f"./pictures/edited_{str(final_picture_size)}/{part_number}"

# create directories if they don't exist
Path(raw_pictures_path).mkdir(parents=True, exist_ok=True)
Path(processed_pictures_path).mkdir(parents=True, exist_ok=True)


def edit_picture(raw_picture):
    gray_frame = cv.cvtColor(raw_picture, cv.COLOR_RGB2GRAY)
    cv.imshow("grey_image", gray_frame)

    mask = cv.inRange(gray_frame, lower_color, upper_color)
    # cv.imshow("mask", mask)

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
    # cv.imshow("contour", contour_image)

    # draw contours and crop image
    if len(contours) > 0:
        contour = contours[0]
        x, y, w, h = cv.boundingRect(contour)
        center = (x + w / 2, y + h / 2)
        center_x, center_y = center

        # convert picture to square by choosing the longer side as side length
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
        # cv.imshow("cropped", cropped_image)

        # resize image
        new_image_dimensions = (final_picture_size, final_picture_size)
        resized_image = cv.resize(cropped_image, new_image_dimensions)
        cv.imshow("resized", resized_image)

        return resized_image

    else:
        # return empty array if no part was found
        return np.array([])


while True:
    # frame = cam.get_frame(cap)
    frame = cv.imread("test_image.png")
    # cv.imshow("raw_image", frame)

    # check if picture is empty else save it
    if (new_picture := edit_picture(frame)).any():
        # save image
        if save_processed_pictures:
            cv.imwrite(processed_pictures_path + f"/{str(current_id)}.png", new_picture)
        if save_raw_pictures:
            cv.imwrite(raw_pictures_path + f"/{str(current_id)}.png", frame)

        if save_raw_pictures or save_processed_pictures:
            current_id += 1
            time.sleep(time_between_pictures)

            if current_id > number_of_pictures:
                break

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
