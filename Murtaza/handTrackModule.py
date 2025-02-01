'''NOTE I replaced this with HandModule.py in Murtaza folder because I could not get this to identify individual hands
Note Save maybe for future reference as lessons proceed.
follow Murtaza's class structure 
Pass true to draw connections and circles
works fine but for one hand
'''
# import tensorflow as tf
# print(tf.config.list_physical_devices('GPU'))

import mediapipe as mp
import sys
import cv2
print(cv2.__version__)
import numpy as np
print(f"This is version {sys.version}")
print(np.__version__)
import time
# import tensorflow as tf
# tf.config.experimental.set_memory_growth(tf.config.list_physical_devices('GPU')[0], True)

class handDetector():
    import mediapipe as mp
    def __init__(self,mode=False,maxHands=2,tol1=.5,tol2=.5):
        ## could do self.mpHands=self.mp.solutions.hands
        ## then     sself.hands=self.mpHands.Hands(mode....)
        self.hands=self.mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, 
     min_tracking_confidence=0.5)
        # self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
        self.mpDraw=self.mp.solutions.drawing_utils
        
    def findHands(self,frame,draw=True):
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)## make results into self.results so can use in the other functions/methods
    # the arrays of hand data come back in results.multi_hand_landmarks.  if = NOne +Go look for more hands.If not nothing then look further
        self.results = self.hands.process(frameRGB)       # call the HANDS object and process it in RGB. reuslts is the object with lots of arrays
        if self.results.multi_hand_landmarks != None:## the data in the multi_hand_landmarks are the arrays of handmarks in the results object, (actually for two hands in our case) 
            for handLandMarks in self.results.multi_hand_landmarks:
                if draw:
            # mpDraw.draw_landmarks(frame,handLandMarks)## we are moving each set of arrays to the method of the mpDraw objects method named 'draw-landmarks'
                    self.mpDraw.draw_landmarks(frame,handLandMarks,mp.solutions.hands.HAND_CONNECTIONS)## we are moving each set of arrays to the method of the mpDraw objects method named 'draw-landmarks'
            # # print(handLandMarks)    ## above the mpDraw draws the landmarks on the frame(in RGB)
        return frame 
 
    def findPosition(self,frame,handNo=0,draw= True):
 
        lmList=[]
        if self.results.multi_hand_landmarks:## the data in the multi_hand_landmarks are the arrays of handmarks in the results object, (actually for two hands in our case) 
            # for handLandMarks in self.results.multi_hand_landmarks:
            # for id,lm in enumerate(handLandMarks.landmark):
            ## the commneted out lines were for landmarks without hand specificity
            myHand=self.results.multi_hand_landmarks[handNo]
            
            # for id,lm in enumerate(handLandMarks.landmark[handNo]):
            for id,lm in enumerate(myHand.landmark):
                
                
                #print(id,lm)
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),15,(125,0,125),cv2.FILLED)
        return lmList

def main():
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

    myDetector=handDetector()
    while True:
        ignore,  frame = cam.read()
        frame=cv2.flip(frame,1)
        frame=myDetector.findHands(frame,True)
        lmList=myDetector.findPosition(frame,0,False)
        if len(lmList)!=0:
            # print(lmList[4])
            id,x,y=lmList[4]
            # print(x,' ',y,' ',id)
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
'''
hands=mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, 
    min_tracking_confidence=0.5)
    the hands after mp.solutions references very specific methods.
     THe .Hands is another method inside of mp.slolutons.hands.
'''
# mpDraw = mp.solutions.drawing_utils     # this is to annotate the frame with the data, if want to analyze the frame TO DRAW HANDS  use the mp.solutions.hands.Hands(   , , )

 