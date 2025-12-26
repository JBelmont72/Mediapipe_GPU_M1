import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
tf.config.experimental.set_memory_growth(tf.config.list_physical_devices('GPU')[0], True)
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
import mediapipe as mp
import sys
import cv2
print(cv2.__version__)
import numpy as np
print(f"This is version {sys.version}")
print(np.__version__)
import time
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Force GPU usage
class handDetector():
    import mediapipe as mp
    def __init__(self,mode=False,maxHands=2,tol1=.5,tol2=.5):
        self.hands=self.mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mpDraw=self.mp.solutions.drawing_utils
        
    def findHands(self,frame,draw=True):
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)
        if self.results.multi_hand_landmarks != None:
            for handLandMarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame,handLandMarks,mp.solutions.hands.HAND_CONNECTIONS)
        return frame 
 
    def findPosition(self,frame,handNo=0,draw= True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),15,(125,0,125),cv2.FILLED)
        return lmList

def main():
    cam = cv2.VideoCapture(0)
    width= 1280
    height= 720
    pTime = 0
    cTime = 0
    filter=25
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
    cam.set(cv2.CAP_PROP_FPS, 30)
    cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

    myDetector=handDetector()
    while True:
        ignore,  frame = cam.read()
        frame=cv2.flip(frame,1)
        frame=myDetector.findHands(frame,True)
        lmList=myDetector.findPosition(frame,0,False)
        if len(lmList)!=0:
            id,x,y=lmList[4]
            cv2.circle(frame,(x,y),20,(255,255,0),2)
            
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
if __name__=='__main__':
    main() 