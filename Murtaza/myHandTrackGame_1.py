'''
import hand tracking module from 'Murtaza/handTrackModule.py'
myDetector=htm.mpHands()

findPosition(self,frame,handNo=0,draw= True)

labelHands(self,frame,myHands,handsType,draw=True)
'''
import mediapipe as mp
import sys
import cv2
print(cv2.__version__)
import numpy as np
print(f"This is version {sys.version}")
print(np.__version__)
import time
## note different ways to call the handDetector module__ if just 'as htm' then need to modify the object creation below
# from handTrackModule import *
# import handTrackModule as htm
# from handTrackModule import handDetector
## replaced with
import HandModule as  htm


cam = cv2.VideoCapture(1)
width= 1280  #640
height= 720  #360
pTime = 0
cTime = 0
filter=25
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
myDetector=htm.mpHands()
# myDetector=handDetector()
while True:
    # print(htm.__name__)
    ignore,  frame = cam.read()
    frame=cv2.flip(frame,1)
    frame,myHands,handsType=myDetector.Marks(frame,False)
    lmList=myDetector.findPosition(frame,0,False) ## or 'draw=False 'if leave out the second arguement
    myDetector.labelHands(frame,myHands,handsType,draw=True)
    if len(lmList)!=0:
        
        print(lmList[4])
        id,x,y=lmList[4]
        print(x,' ',y,' ',id)
        cv2.circle(frame,(x,y),20,(255,255,0),2)
        cv2.putText(frame,'my Thumb!',(x,y),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,2,(255,0,255))
        
    cTime=time.time()
    fps=1/(cTime-pTime)
    Filtfps=filter*.95 +fps*.05
    pTime=cTime
    Filtfps=str(int(Filtfps))
    cv2.putText(frame,(Filtfps+'fps'),(20,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
    
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('c'):
        break
cam.release()