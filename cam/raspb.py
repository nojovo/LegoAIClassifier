from picamera2 import Picamera2

def capture():
    capturer = Picamera2()
    capturer.start
    return capturer

def get_frame(capture):
    frame = capture.capture_array
    return frame
