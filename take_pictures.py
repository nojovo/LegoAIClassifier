import logging
import cv2 as cv
import cam

logging.basicConfig(level=logging.DEBUG)
logging.debug("Current os: " + cam.os_type)

lower_color = 0
upper_color = 5
connectivity = 4

cap = cam.capture()


while True:
    frame = cam.get_frame(cap)

    gray_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    thresh = cv.threshold(gray_frame, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    # mask = cv.inRange(gray_frame, lower_color, upper_color)
    # masked_image = cv.bitwise_and(frame, frame, mask=mask)
    output = cv.connectedComponentsWithStats(thresh, connectivity, cv.CV_32S)
    (numLabels, labels, stats, centroids) = output

    for i in range(0, numLabels):
        logging.info("Current component: " + str(i + 1) + "/" + str(numLabels))

        x = stats[i, cv.CC_STAT_LEFT]
        y = stats[i, cv.CC_STAT_TOP]
        w = stats[i, cv.CC_STAT_WIDTH]
        h = stats[i, cv.CC_STAT_HEIGHT]
        area = stats[i, cv.CC_STAT_AREA]
        (cX, cY) = centroids[i]

        output = frame.copy()
        cv.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)

        cv.imshow("raw_image", frame)
        cv.imshow("grey_image", gray_frame)
        cv.imshow("thresh", thresh)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

