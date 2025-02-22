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

    while True:
        ret, frame = cam.read()
        frame = cv2.resize(frame, (width, height))
        frame = cv2.flip(frame, 1)
        frame, handsLM, handsType = findHands.Marks(frame, draw=True)
        # all_lmLists = findHands.findPositions(frame, draw=False)  # Get landmarks without drawing here

        # # Loop over each hand's landmarks along with its type
        # for lmList, handType in zip(all_lmLists, handsType):
        #     if handType == 'Right':
        #         # Draw blue circles for right hand landmarks
        #         for id, cx, cy in lmList:
        #             cv2.circle(frame, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
        #     elif handType == 'Left':
        #         # Draw green circles for left hand landmarks
        #         for id, cx, cy in lmList:
        #             cv2.circle(frame, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            
        
        
        
        right_hand_coords, left_hand_coords = findHands.labelHands(frame, handsLM, handsType)
        if handsLM:  # Only proceed if any hands are detected
            lmList = findHands.findPositions(frame, draw=False)
            if lmList:
                print(lmList)
        
        if right_hand_coords:
            # Perform action for right hand
            cv2.circle(frame, right_hand_coords, 20, (255, 0, 0), 2)  # Blue circle for right hand

        if left_hand_coords:
            # Perform action for left hand
            cv2.circle(frame, left_hand_coords, 20, (0, 255, 0), 2)  # Green circle for left hand

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
    
    
    
    
    
    
    
    
    
#     import mediapipe as mp
#     def __init__(self,mode=False,maxHands=2,tol1=.5,tol2=.5):
#         ## could do self.mpHands=self.mp.solutions.hands
#         ## then     sself.hands=self.mpHands.Hands(mode....)
#         self.hands=self.mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, 
#      min_tracking_confidence=0.5)
#         # self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
#         self.mpDraw=self.mp.solutions.drawing_utils
#         def Marks(self,frame,draw=False):
#         myHands=[]
#         handsType=[]
#         frameRGB=cv2.cvtColor(,cv2.COLOR_BGR2RGB)
#         self.results=self.hands.process(frameRGB)
#         if self.results.multi_hand_landmarks != None:
#             #print(results.multi_handedness)
#             for hand in self.results.multi_handedness:
#                 #print(hand)
#                 #print(hand.classification)
#                 #print(hand.classification[0])
#                 handType=hand.classification[0].label
#                 handsType.append(handType)
#             for handLandMarks in self.results.multi_hand_landmarks:
                
#                 myHand=[]
#                 for landMark in handLandMarks.landmark:
#                     myHand.append((int(landMark.x*self.width),int(landMark.y*self.height)))
#                 myHands.append(myHand)
#                 if draw:
#                     self.mpDraw.draw_landmarks(frame,handLandMarks,self.mp.solutions.hands.HAND_CONNECTIONS)
#         return frame,myHands,handsType
   
#     # def findHands(self,frame,draw=True):
#     #     frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)## make results into self.results so can use in the other functions/methods
#     # # the arrays of hand data come back in results.multi_hand_landmarks.  if = NOne +Go look for more hands.If not nothing then look further
#     #     self.results = self.hands.process(frameRGB)       # call the HANDS object and process it in RGB. reuslts is the object with lots of arrays
#     #     if self.results.multi_hand_landmarks != None:## the data in the multi_hand_landmarks are the arrays of handmarks in the results object, (actually for two hands in our case) 
#     #         for handLandMarks in self.results.multi_hand_landmarks:
#     #             if draw:
#     #         # mpDraw.draw_landmarks(frame,handLandMarks)## we are moving each set of arrays to the method of the mpDraw objects method named 'draw-landmarks'
#     #                 self.mpDraw.draw_landmarks(frame,handLandMarks,mp.solutions.hands.HAND_CONNECTIONS)## we are moving each set of arrays to the method of the mpDraw objects method named 'draw-landmarks'
#     #         # # print(handLandMarks)    ## above the mpDraw draws the landmarks on the frame(in RGB)
#     #     return frame 
 
#     def findPosition(self,frame,handNo=0,draw= True):
 
#         lmList=[]
#         if self.results.multi_hand_landmarks:## the data in the multi_hand_landmarks are the arrays of handmarks in the results object, (actually for two hands in our case) 
#             # for handLandMarks in self.results.multi_hand_landmarks:
#             # for id,lm in enumerate(handLandMarks.landmark):
#             ## the commneted out lines were for landmarks without hand specificity
#             myHand=self.results.multi_hand_landmarks[handNo]
            
#             # for id,lm in enumerate(handLandMarks.landmark[handNo]):
#             for id,lm in enumerate(myHand.landmark):
                
                
#                 #print(id,lm)
#                 h,w,c=frame.shape
#                 cx,cy=int(lm.x*w),int(lm.y*h)
#                 lmList.append([id,cx,cy])
#                 if draw:
#                     cv2.circle(frame,(cx,cy),15,(125,0,125),cv2.FILLED)
#         return lmList
#     def labelHands(self, frame, myHands, handsType, draw=True):
#         right_hand_coords = None
#         left_hand_coords = None
#         for hand, handType in zip(myHands, handsType):
#             if handType == 'Right':
#                 right_hand_coords = hand[8]  # Index finger tip
#                 if draw:
#                     cv2.putText(frame, 'Right', hand[8], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
#             elif handType == 'Left':
#                 left_hand_coords = hand[8]  # Index finger tip
#                 if draw:
#                     cv2.putText(frame, 'Left', hand[8], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
#         return right_hand_coords, left_hand_coords


# def main():
#     cam = cv2.VideoCapture(1)
#     width= 1280  #640
#     height= 720  #360
#     pTime = 0
#     cTime = 0
#     filter=25
#     cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#     cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
#     cam.set(cv2.CAP_PROP_FPS, 30)
#     cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

#     myDetector=handDetector()
#     while True:
#         ignore,  frame = cam.read()
#         frame=cv2.flip(frame,1)
#         frame=myDetector.findHands(frame,True)
#         lmList=myDetector.findPosition(frame,0,True)
#         frame, handsLM, handsType = myDetector.Marks(frame, True)
#         right_hand_coords, left_hand_coords = myDetector.labelHands(frame, handsLM, handsType)

#         if right_hand_coords:
#             # Perform action for right hand
#             cv2.circle(frame, right_hand_coords, 20, (255, 0, 0), 2)  # Blue circle for right hand

#         if left_hand_coords:
#             # Perform action for left hand
#             cv2.circle(frame, left_hand_coords, 20, (0, 255, 0), 2)  # Green circle for left hand

            
#         cTime=time.time()
#         fps=1/(cTime-pTime)
#         Filtfps=filter*.95 +fps*.05
#         pTime=cTime
#         Filtfps=str(int(Filtfps))
#         cv2.putText(frame,(Filtfps+'fps'),(20,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
        
#         cv2.imshow('my WEBcam', frame)
#         cv2.moveWindow('my WEBcam',0,0)
#         if cv2.waitKey(1) & 0xff ==ord('c'):
#             break
#     cam.release()
# if __name__=='__main__':
#     main()   
# '''
# hands=mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, 
#     min_tracking_confidence=0.5)
#     the hands after mp.solutions references very specific methods.
#      THe .Hands is another method inside of mp.slolutons.hands.
# '''
# # mpDraw = mp.solutions.drawing_utils     # this is to annotate the frame with the data, if want to analyze the frame TO DRAW HANDS  use the mp.solutions.hands.Hands(   , , )

 