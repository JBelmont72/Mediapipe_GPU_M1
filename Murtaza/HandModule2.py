'''handTrackModule.py is the most up to date
To differentiate between actions for the right and left hands in your program, you can modify the labelHands method to return the coordinates of specific landmarks for each hand. This will allow you to perform distinct actions based on the hand type. Here's how you can adjust your code:

Modify the labelHands Method: Update this method to return the coordinates of a specific landmark (e.g., the tip of the index finger) for both the right and left hands.

Update the main Function: In your main loop, capture the returned coordinates and perform actions based on which hand is detected.


'''




import cv2
print(cv2.__version__)
import time

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

    def findPosition(self,frame,handNo=0,draw= True):
 
        lmList=[]
        if self.results.multi_hand_landmarks:## the data in the multi_hand_landmarks are the arrays of handmarks in the results object, (actually for two hands in our case) 
            # for handLandMarks in self.results.multi_hand_landmarks:
            # for id,lm in enumerate(handLandMarks.landmark):
            ## the commented out lines were for landmarks without hand specificity
            myHand=self.results.multi_hand_landmarks[handNo]
            
            # for id,lm in enumerate(handLandMarks.landmark[handNo]):
            for id,lm in enumerate(myHand.landmark):
                
                
                # print(id,lm)
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),15,(125,0,125),cv2.FILLED)
        return lmList

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



    # def labelHands(self,frame,myHands,handsType,draw=True): ###my old
    #     for hand,handType in zip(myHands,handsType):
    #         if handType=='Right':
    #             lblR='Right'
    #             print('this is my ',lblR)
    #             if draw:        
    #                 cv2.putText(frame,lblR,hand[8],cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
    #     for hand,handType in zip(myHands,handsType):        
    #         if handType=='Left':
    #             lblL='Left'
    #             print('this is my ',lblL)
    #             print(hand[8])
    #             if draw:
    #                 cv2.putText(frame,lblL,hand[8],cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)

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
        frame, handsLM, handsType = findHands.Marks(frame, True)
        right_hand_coords, left_hand_coords = findHands.labelHands(frame, handsLM, handsType)
        print(right_hand_coords)
        if handsLM:  # Only proceed if any hands are detected
            lmList = findHands.findPosition(frame, handNo=0, draw=True)
            if lmList:
                print(lmList)
                
        
        
        # lmList = findHands.findPosition(frame, handNo=0, draw=True)

        # if lmList != None:
        #     print(lmList)
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