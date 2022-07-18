import cv2
import numpy as np
import math
space = [800,800]



image = cv2.imread('eggPic3.jpg')
#cv2.imshow("HoughCirlces", planets)
scale_percent = 70  # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
image=resized


cv2.imshow("No filter", image)


gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray_img", gray_img)

img = cv2.medianBlur(gray_img, 5)
cv2.imshow("medianBlur", img)

ret,threshreal = cv2.threshold(gray_img,127,255,cv2.THRESH_BINARY)
ret,threshblure = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

edged = cv2.Canny(threshblure, 30, 200)


cv2.imshow("binary- no blure", threshreal)
cv2.imshow("binary- after blure", threshblure)
cv2.imshow("edged", edged)

contours, hierarchy = cv2.findContours(threshblure, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(image, contours, -1, (0,0,255), 3)
cv2.imshow("contour", image)



for i in range(len(contours)):
    cnt = contours[i]
    if (cv2.contourArea(cnt) > 1500):  # fillter the worng shape
        M = cv2.moments(cnt)#find data of countor
        cx = int(M['m10']/M['m00'])#center of area
        cy = int(M['m01']/M['m00'])#center of area
        ellipse = cv2.fitEllipse(cnt)
        image = cv2.ellipse(image,ellipse,(0,0,255),5)# create ellipse around circle
        angl=math.pi-ellipse[2]*math.pi/180# create cast for the coordienate system and convert to radian
        line_length=100
        cx2=int(cx + line_length * np.sin(angl))# x end point line
        cy2=int(cy + line_length * np.cos(angl))# y end point line
        image=cv2.line(image, (cx,cy), (cx2,cy2),(0,0,255),4)# create angle line on image
        cv2.putText(image, str((cx,cy)),(cx,cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 255), 2, cv2.LINE_AA)
        cv2.putText(image, "angle: "+str(round(ellipse[2], 2)),(cx-20,cy+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200, 255), 2, cv2.LINE_AA)
        image = cv2.circle(image, (cx,cy), 3, (0,0,255),3)# create point in centroid



#print(circles[0][1])
cv2.imshow("HoughCirlces", image)
cv2.waitKey()
cv2.destroyAllWindows()