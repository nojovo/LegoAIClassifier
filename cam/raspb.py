from picamera2 import Picamera2
import logging

logging.basicConfig(level=logging.ERROR)


def capture():
    capturer = Picamera2()
    capturer.start()
    return capturer


def get_frame(capture):
    frame = capture.capture_array()
    return frame
