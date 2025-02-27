'''
this is a copy in the FINGER CONTROL FOLDER  becasue I need it to be accessible for importing.
NOTE that if I want to utilize left right handedness, I should use the HandModule.py that is the MURTAZA folder
import mediapipe as mp
import sys
import cv2
print(cv2.__version__)
import numpy as np
print(f"This is version {sys.version}")
print(np.__version__)
import time

import handTrackModule as htm
from htm import mpHands
myObject=htm()
frame,myHands,handsType=myObject.Marks(frame,draw=False)
all_lmLists=myObject.findPostions(frame,draw=False)
right_hand_coords, left_hand_coords   =myObject.labelHands(self, frame, myHands, handsType, draw=True)
def main():
    import cv2
    import time
    width = 1280
    height = 720
    cam = cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_FPS, 30)
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    findHands = mpHands(2)
    pTime = 0

    while True:
        ret, frame = cam.read()
        frame = cv2.resize(frame, (width, height))
        frame = cv2.flip(frame, 1)
        frame, handsLM, handsType = findHands.Marks(frame, draw=True)
        right_hand_coords, left_hand_coords = findHands.labelHands(frame, handsLM, handsType)
        if handsLM:  # Only proceed if any hands are detected
            lmList = findHands.findPositions(frame, draw=False)
            if lmList:
                print(lmList)
        
        if right_hand_coords:
            # Perform action for right hand
            cv2.circle(frame, right_hand_coords, 20, (255, 0, 0), 2)  # Blue circle for right hand

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
# class handDetector():
class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=.5,tol2=.5):
        self.width=1280
        self.height=720
        self.hands=self.mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, 
     min_tracking_confidence=0.5)
        # self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
        self.mpDraw=self.mp.solutions.drawing_utils
    def Marks(self,frame,draw=False):
        myHands=[]
        handsType=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(frameRGB)
        if self.results.multi_hand_landmarks != None:
            #print(results.multi_handedness)
            for hand in self.results.multi_handedness:
                #print(hand)
                #print(hand.classification)
                #print(hand.classification[0])
                handType=hand.classification[0].label
                handsType.append(handType)
            for handLandMarks in self.results.multi_hand_landmarks:
                
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*self.width),int(landMark.y*self.height)))
                myHands.append(myHand)
                if draw:
                    self.mpDraw.draw_landmarks(frame,handLandMarks,self.mp.solutions.hands.HAND_CONNECTIONS)
        return frame,myHands,handsType

    def findPositions(self, frame, draw=True):
    # Processes all detected hands and returns a list where each element is the landmark list for a hand.
    
        all_lmLists = []
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                lmList = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                    if draw:
                        # Here you could draw with a generic color.
                        cv2.circle(frame, (cx, cy), 15, (125, 0, 125), cv2.FILLED)
                all_lmLists.append(lmList)
        return all_lmLists

    def labelHands(self, frame, myHands, handsType, draw=True):
        right_hand_coords = None
        left_hand_coords = None
        for hand, handType in zip(myHands, handsType):
            if handType == 'Right':
                right_hand_coords = hand[8]  # Index finger tip
                if draw:
                    cv2.putText(frame, 'Right', hand[8], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
            elif handType == 'Left':
                left_hand_coords = hand[8]  # Index finger tip
                if draw:
                    cv2.putText(frame, 'Left', hand[8], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        return right_hand_coords, left_hand_coords

def main():
    import cv2
    import time
    width = 1280
    height = 720
    cam = cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_FPS, 30)
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    findHands = mpHands(2)
    pTime = 0
    keyPoints=[4,8,12,16,20]
    while True:
        ret, frame = cam.read()
        frame = cv2.resize(frame, (width, height))
        frame = cv2.flip(frame, 1)
        frame, handsLM, handsType = findHands.Marks(frame, draw=False)
        all_lmLists = findHands.findPositions(frame, draw=False)  # Get landmarks without drawing here [[0,322,739,...]]
        for hand,handType in zip(handsLM,handsType):## gives left and/or rignt and tuple
            print(hand,handType)
            if handType == 'Left':
                print(hand[8])
                cv2.circle(frame,hand[8],30,(255,0,0),3)
                for ind in keyPoints:
                    cv2.circle(frame,hand[ind],25,(255,0,255),3)
         
         
            
        # Loop over each hand's landmarks along with its type, uses handsType from .Marks() and all_lmLists from .findPositions()
        for lmList, handType in zip(all_lmLists, handsType):   ## all_lmLists contains [[0,22,234],...]
            if handType == 'Right':
                # Draw blue circles for right hand landmarks
                # for id in keyPoints:
                for id, cx, cy in lmList:
                
                    # print(id,cx,cy)     
                    cv2.circle(frame, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
            elif handType == 'Left':
                # Draw green circles for left hand landmarks
                for id, cx, cy in lmList:
                    cv2.circle(frame, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        ###~~~~~~~~~~~
        # right_hand_coords, left_hand_coords = findHands.labelHands(frame, handsLM, handsType)## .labelHands() uses .Marks()
        # if handsLM:  # Only proceed if any hands are detected
        #     lmList = findHands.findPositions(frame, draw=False)
        #     if lmList:
        #         print(lmList)
        
        # if right_hand_coords:
        #     # Perform action for right hand
        #     cv2.circle(frame, right_hand_coords, 20, (255, 0, 0), 2)  # Blue circle for right hand

        # if left_hand_coords:
        #     # Perform action for left hand
        #     cv2.circle(frame, left_hand_coords, 20, (0, 255, 0), 2)  # Green circle for left hand

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv2.imshow('my WEBcam', frame)
        cv2.moveWindow('my WEBcam', 0, 0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
    
    
'''
hands=mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, 
    min_tracking_confidence=0.5)
    the hands after mp.solutions references very specific methods.
     THe .Hands is another method inside of mp.slolutons.hands.
'''
# mpDraw = mp.solutions.drawing_utils     # this is to annotate the frame with the data, if want to analyze the frame TO DRAW HANDS  use the mp.solutions.hands.Hands(   , , )   
    
    
 