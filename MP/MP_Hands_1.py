'''
my version of the basic Hand landmark finder , used enumerate and zip functions
'''
import mediapipe as mp
import sys
import cv2
print(cv2.__version__)
import numpy as np
print(f"This is version {sys.version}")
print(np.__version__)
width= 1280  #640
height= 720  #360
cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
hands=mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, 
    min_tracking_confidence=0.5)
'''
hands=mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, 
    min_tracking_confidence=0.5)
    the hands after mp.solutions references very specific methods.
     THe .Hands is another method inside of mp.slolutons.hands.
'''
mpDraw = mp.solutions.drawing_utils     # this is to annotate the frame with the data, if want to analyze the frame TO DRAW HANDS  use the mp.solutions.hands.Hands(   , , )
myIndex=[]
myHand=[]
while True:
    ignore,  frame = cam.read()
    frame = cv2.resize(frame,(width,height))
    frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # the arrays of hand data come back in results.multi_hand_landmarks.  if = NOne +Go look for more hands.If not nothing then look further
    results = hands.process(frameRGB)       # call the HANDS object and process it in RGB. reuslts is the object with lots of arrays
    if results.multi_hand_landmarks != None:## the data in the multi_hand_landmarks are the arrays of handmarks in the results object, (actually for two hands in our case) 
        for handLandMarks in results.multi_hand_landmarks:
            # mpDraw.draw_landmarks(frame,handLandMarks)## we are moving each set of arrays to the method of the mpDraw objects method named 'draw-landmarks'
            mpDraw.draw_landmarks(frame,handLandMarks,mp.solutions.hands.HAND_CONNECTIONS)## we are moving each set of arrays to the method of the mpDraw objects method named 'draw-landmarks'
            # print(handLandMarks)    ## above the mpDraw draws the landmarks on the frame(in RGB)
            myHand=[]
            myIndex=[]
            for (index,landMark)in enumerate(handLandMarks.landmark):
                # print(index,landMark)
                
                # print(index,int(landMark.x*width),int(landMark.y*height))
                myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myIndex.append(index)
            print(myHand)
            print(myIndex)
    for (I,H) in zip(myIndex,myHand):
        if I==4:
            cv2.circle(frame,H,15,(255,0,255),3)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('c'):
        break
cam.release()