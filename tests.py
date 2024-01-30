from pathlib import Path
from process_pictures import edit_picture
import cv2 as cv

raw_path = "./pictures/raw/2780/1.png"
processed_pictures_path = f"./pictures/edited_100/32316/1.png"

frame = cv.imread(raw_path)

new_frame = edit_picture(frame)

cv.imwrite(processed_pictures_path, new_frame)


