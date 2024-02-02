import cam
import keras
import tensorflow as tf
import cv2 as cv
from process_pictures import edit_picture
import numpy as np


parts = ["32316", "32140", "32270", "2780", "32073"]

# cap = cam.capture()
cap = cv.VideoCapture("rtsp://192.168.137.26:8554/cam")

# lite_interpreter = tf.lite.Interpreter(model_path="models/model3.tflite")
# print(lite_interpreter.get_signature_list())
# classify = lite_interpreter.get_signature_runner("serving_default")

keras_model = keras.models.load_model("models/model3.keras")


# def classify_lite(input_picture):
#     predictions = classify(input_1=input_picture)["dense"]
#     return predictions


def classify_keras(input_picture):
    predictions = keras_model.predict(input_picture, verbose=0)
    return predictions


print("\n\n")

while True:
    # frame = cam.get_frame(cap)
    ret, frame = cap.read()
    # frame = cv.imread("test_image.png")

    if ret:
        if (new_picture := edit_picture(frame)).any():
            image = cv.resize(new_picture, (128, 128))
            image_array = keras.utils.img_to_array(image)
            image_array = tf.expand_dims(image_array, 0)

            prediction = classify_keras(image_array)
            print(f"{parts[np.argmax(prediction)]}: {round(100 * np.max(prediction), 2)}%", end="\r")
        else:
            print("nothing found", end="\r")

    if cv.waitKey(1) == ord("q"):
        break


cv.destroyAllWindows()
cap.release()
