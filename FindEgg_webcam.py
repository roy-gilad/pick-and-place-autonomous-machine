import cv2
import math
import numpy as np
import serial
import time


def SendToArduino(x,y,a):

    #  calibration
    x=int((x-181)/2)+10
    y=int((y-16)/2)
    a=int(a)
    if a>0 and a<=90:
        a=a+90
    elif a>90:
        a=a-90
    string = 'X{0:d}Y{1:d}A{2:d}'.format((x), (y),(a))
    ser.write(string.encode('utf-8'))
    #time.sleep(1)
    data = ser.readline()
    print(data.decode('utf-8'))


cap = cv2.VideoCapture(1)# 1 for web cam. 0 for computer camera



# serial communicate
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(1)
data=ser.readline()

#create list to store cordinate and angle data for each frame
x_list=[]
y_list=[]
angle_list=[]

while(True):
    ret, frame = cap.read()



    blur = cv2.blur(frame, (7, 7))
    ret, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_TRUNC)

    # Find Canny edges
    edged = cv2.Canny(thresh, 30, 200)


    # Finding Contours
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #run all the close contors

    for i in range(len(contours)):
        cnt = contours[i]
        if(cv2.contourArea(cnt)>8500 and cv2.contourArea(cnt)<10000):

            M = cv2.moments(cnt)#find data of countor
            cx = int(
                M['m10']/M['m00'])#center of area
            cy = int(M['m01']/M['m00'])#center of area
            x_list.append(cx)
            y_list.append(cy)
           # print(cx,cy)


            ellipse = cv2.fitEllipse(cnt)
            image = cv2.ellipse(frame,ellipse,(0,0,255),5)# create ellipse around circle
            angl=math.pi-ellipse[2]*math.pi/180# create cast for the coordienate system and convert to radian

            line_length=100
            cx2=int(cx + line_length * np.sin(angl))# x end point line
            cy2=int(cy + line_length * np.cos(angl))# y end point line
            frame=cv2.line(frame, (cx,cy), (cx2,cy2),(0,0,255),4)# create angle line on image
            cv2.putText(frame, str((cx,cy)),(cx,cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "angle: "+str(round(ellipse[2])),(cx-20,cy+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200, 255), 2, cv2.LINE_AA)
            angle_list.append(ellipse[2])
            frame = cv2.circle(frame, (cx,cy), 1, (0,0,255),3)# create point in centroid

    #send the data just one  coordinate
    if x_list:
        Xmin_index=y_list.index(min(y_list)) # Send the closest (max of y) egg to the carton

        SendToArduino(x_list[Xmin_index], y_list[Xmin_index],angle_list[Xmin_index])  # send cordinate to arduino
        x_list.clear()
        y_list.clear()
        angle_list.clear()



    # Draw all contours
    # -1 signifies drawing all contours, else draw not all contor
    cv2.drawContours(frame, contours,-1, (0, 255, 0), 3)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()