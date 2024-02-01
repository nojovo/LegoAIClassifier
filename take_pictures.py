import logging
from pathlib import Path
import cv2 as cv
import cam
from process_pictures import edit_picture

parts = ["32316", "32140", "32270", "2780", "32073"]

part_number = parts[0]
current_id = 1
end_id = 10
save_raw_pictures = True
save_processed_pictures = False

cap = cam.capture()

raw_pictures_path = f"./pictures/raw/{part_number}"
processed_pictures_path = f"./pictures/edited/{part_number}"

# create directories if they don't exist
Path(raw_pictures_path).mkdir(parents=True, exist_ok=True)
Path(processed_pictures_path).mkdir(parents=True, exist_ok=True)


while current_id < end_id:
    frame = cam.get_frame(cap)
    # frame = cv.imread("test_image.png")
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
            print(current_id)

    if cv.waitKey(1) == ord("q"):
        break

cv.destroyAllWindows()
cap.release()
