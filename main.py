import cv2
import numpy as np
import pprint
import sys
import datetime
import math
import cv2


img = cv2.imread('ff.jpg')

# cv2.imshow("HoughCirlces", img)
# ret, thresh = cv2.threshold(img, 127, 255, 0)
# contours, hierarchy = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow("rs", img)

cv2.imshow("Loggers", thresh)

for i in range(len(contours)):
    contour = contours[i]

    if len(contour) >= 5:
        print(contour)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        radius = int(radius)
        (x, y, w, h) = cv2.boundingRect(contour)

        ellipse = cv2.fitEllipse(contour)
        (center, axis, angle) = ellipse
        coordXContour, coordYContour = int(center[0]), int(center[1])
        coordXCentroid = (2 * coordXContour + w) // 2
        coordYCentroid = (2 * coordYContour + h) // 2
        ax1, ax2 = int(axis[0]) - 2, int(axis[1]) - 2
        orientation = int(angle)
        area = cv2.contourArea(contour)
        print(area)
        cv2.ellipse(thresh, (coordXContour, coordYContour), (ax1, ax2), orientation, 0, 360,(255, 0, 0), 2)  # blue

cv2.imshow("Loggers", thresh)

cv2.waitKey()
cv2.destroyAllWindows()