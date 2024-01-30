from picamera2 import Picamera2
import logging

logging.basicConfig(level=logging.ERROR)

camera = Picamera2()
config = camera.create_video_configuration()
camera.configure(config)
camera.set_controls({"Brightness": 0.2})


def capture():
    capturer = Picamera2()
    capturer.start()
    return capturer


def get_frame(capturer):
    frame = capturer.capture_array()
    return frame
