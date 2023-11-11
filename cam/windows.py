from cv2 import VideoCapture


def capture():
    cap = VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    return cap


def get_frame(capture):
    ret, frame = capture.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        exit()
    return frame
