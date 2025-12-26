import osascript
import cv2
import time
import numpy as np
import HandModule as htm
# import handTrackModule as htm
import math
# from ctypes import cast, POINTER
################################
wCam, hCam = 640, 480
################################
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
# detector = htm.handDetector()
detector = htm.mpHands(0.5,0.5) ## created the object calling the class in the module

# minVol = volRange[0]
# maxVol = volRange[1]
import osascript
# target_volume = 50
# osascript.osascript("set volume output volume {}".format(target_volume))
minVol = 0
maxVol = 100
vol = 0
volBar = 400
volPer = 0
while True:
    success, img = cap.read()
    frame,myHands,handsType = detector.Marks(img,True)## only using the img in this case 
    
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2=  lmList[8][1], lmList[8][2]
        x3=int((x1+x2)/2)    ## this is the x midpoint
        y3=int((y1+y2)/2 )   ## this is the y midpoint
        # print(x1,y1)
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),4)
        cv2.circle(img,(x1,y1),15,(255,0,0),-1)
        cv2.circle(img,(x2,y2),15,(255,0,0),-1)
        cv2.circle(img,(x3,y3),15,(0,255,0),-1)
        length =math.sqrt((abs(x1-x2)/2)**2+ (abs((y1-y2)/2)**2))
        # print(length)
        vol=.67*length
        print(vol)
        if vol>= 95:
            vol=100
            cv2.putText(img,'Too loud. Turn it down!',(30,110),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        if vol<=15:
            vol=0
            cv2.circle(img,(x3,y3),20,(255,0,255),-1)        
    osascript.osascript("set volume output volume {}".format(vol))
        # volume.SetMasterVolumeLevel(vol, None)
    # if length < 50:
    #     cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (50, 150), (85, 350), (255, 0, 0), 3)
    cv2.rectangle(img, (50, 350), (85,int(350-(2*vol)) ), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(vol)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)