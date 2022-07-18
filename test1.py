import cv2
image = cv2.imread('eggPic4.jpg')
cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()