import cv2
import cv2
import math
import numpy as np

import numpy as np

# Let's load a simple image with 3 black squares
image = cv2.imread('eggPic5.jpeg')

scale_percent = 70  # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
image=resized
cv2.imshow('no filter', image)
# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
cv2.imshow('thresh', thresh)
blur = cv2.blur(image, (5, 5))

#ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_TRUNC)


cv2.imshow('thresh binary', thresh)


# Find Canny edges
edged = cv2.Canny(thresh, 30, 200)


# Finding Contours
# Use a copy of the image e.g. edged.copy()
# since findContours alters the image
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#run all rhe close contors

x_list=[]
y_list=[]

for i in range(len(contours)):
    cnt = contours[i]
    if(cv2.contourArea(cnt)>1500):#fillter the worng shape

        M = cv2.moments(cnt)#find data of countor
        cx = int( M['m10']/M['m00'])#center of area
        cy = int(M['m01']/M['m00'])#center of area
        x_list.append(cx)
        y_list.append(cy)
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
print(x_list)
print(max(x_list))
print(x_list[1])


#print("cos (0) = " + str(np.cos(0)))
#print("Number of Contours found = " + str(len(contours)))

# Draw all contours
# -1 signifies drawing all contours, else draw not all contor
cv2.drawContours(image, contours,-1, (0, 255, 0), 3)

cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()