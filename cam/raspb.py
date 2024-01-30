from picamera2 import Picamera2
from time import sleep
import logging

logging.basicConfig(level=logging.ERROR)

camera = PiCamera(resolution=(1280, 720), framerate=30)
# Set ISO to the desired value
camera.iso = 100
# Wait for the automatic gain control to settle
sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g


def capture():
    capturer = Picamera2()
    capturer.start()
    return capturer


def get_frame(capturer):
    frame = capturer.capture_array()
    return frame
