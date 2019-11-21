import cv2
import numpy as np 

def nothing(x):
    pass

cap =cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")
 
cv2.createTrackbar("B", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("G", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("R", "Trackbars", 0, 255, nothing)


while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    B = cv2.getTrackbarPos("B", "Trackbars")
    G = cv2.getTrackbarPos("G", "Trackbars")
    R = cv2.getTrackbarPos("R", "Trackbars")

    green = np.uint8([[[B, G, R]]])
    hsvGreen = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
    lowerLimit = np.uint8([hsvGreen[0][0][0]-10,100,100])
    upperLimit = np.uint8([hsvGreen[0][0][0]+10,255,255])

    mask = cv2.inRange(hsv, lowerLimit, upperLimit)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    (contours,_) = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if(area > 250):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)



    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(1)
    
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
