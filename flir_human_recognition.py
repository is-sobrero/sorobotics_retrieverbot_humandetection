import cv2
import numpy as np
def empty(a):
    pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(area)
        if (area>3 and area<250):                #tra 5 e 250
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)

            if (peri>300.0 and peri<2000.0):
                approx = cv2.approxPolyDP(cnt,0.02*peri,True)
                print(peri)
                objCor = len(approx)
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(imgResult, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
#cap = cv2.VideoCapture(0)
cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",40,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",60,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars",179,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)


while True:
    #success, img = cap.read()
    img=cv2.imread("Resources/t2.jpg")
    imgR=cv2.resize(img,(700,500))
    imgHSV= cv2.cvtColor(imgR,cv2.COLOR_BGR2HSV)
    h_min=cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    #print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult=cv2.bitwise_and(imgR,imgR,mask=mask)

    #cv2.imshow("imgHSV", imgHSV)
    #cv2.imshow("mask",mask)
    #cv2.imshow("result",imgResult)
    imgResultCanny= cv2.Canny(imgR,200,200)
    getContours(imgResultCanny)
    imgStack= stackImages (0.6,([imgR,imgHSV],[imgResultCanny,imgResult]))
    cv2.imshow("imagestack",imgStack)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break