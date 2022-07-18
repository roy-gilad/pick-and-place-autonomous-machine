#Face tracker using OpenCV and Arduino
#by Shubham Santosh
#
# import cv2
# import serial
# import time
# ArduinoSerial = serial.Serial('COM3', 9600,timeout=1)
#
# time.sleep(10)
#
# while True:
#     data = b'hello word'
#     print(data)
#     ArduinoSerial.write(data)
#     time.sleep(1)

import serial
import time
import cv2
import matan
import FindEgg_webcam

def getCenterOFmass(i):
    cnt = matan.contours[i]
    M = cv2.moments(cnt)#find data of countor
    cx = int(M['m10']/M['m00'])#center of area
    cy = int(M['m01']/M['m00'])#center of area
    return  {'x':cx,'y':cy}




ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(1)
data=ser.readline()

# x=12
# y=15
# print(x,y)
# string = 'X{0:d}Y{1:d}'.format((x), (y))
# ser.write(string.encode('utf-8'))
# time.sleep(1)
# data = ser.readline()
# time.sleep(1)
# print(data.decode('utf-8'))

for i in range(len(matan.contours)):

    # x = getCenterOFmass(i)['x']
    # y = getCenterOFmass(i)['y']
    x=FindEgg_webcam.cx
    y=FindEgg_webcam.cy
    print(x,y)
    string = 'X{0:d}Y{1:d}'.format((x), (y))
    ser.write(string.encode('utf-8'))
    #time.sleep(1)
    data = ser.readline()
    print(data.decode('utf-8'))


