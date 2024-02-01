import cam
import keras
import tensorflow as tf
import cv2 as cv
from process_pictures import edit_picture
import numpy as np


parts = ["32316", "32140", "32270", "2780", "32073"]

cap = cam.capture()

lite_interpreter = tf.lite.Interpreter(model_path="models/model3.tflite")
print(lite_interpreter.get_signature_list())
classify = lite_interpreter.get_signature_runner("serving_default")


def classify_lite(input_picture):
    predictions = classify(rescaling_input=input_picture)["dense"]
    return predictions


print("\n\n")

while True:
    # frame = cam.get_frame(cap)
    frame = cv.imread("test_image.png")

    if (new_picture := edit_picture(frame)).any():
        image = cv.resize(new_picture, (128, 128))
        image_array = keras.utils.img_to_array(image)
        image_array = tf.expand_dims(image_array, 0)

        prediction = classify_lite(image_array)
        print(f"{parts[np.argmax(prediction)]}: {round(100 * np.max(prediction), 2)}%")
    else:
        print("nothing found")

    if cv.waitKey(1) == ord("q"):
        break

cv.destroyAllWindows()
cap.release()
