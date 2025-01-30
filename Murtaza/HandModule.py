'''
functions in module  Marks(self,frame,draw=False):

            findPosition(self,frame,handNo=0,draw= True)

                
                labelHands(self,frame,myHands,handsType,draw=True):
                
                frame,handsLM,handsType=findHands.Marks(frame,True)
    lmList=findHands.findPosition(frame,0,True)
    findHands.labelHands(frame,handsLM,handsType)
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
            ## the commneted out lines were for landmarks without hand specificity
            myHand=self.results.multi_hand_landmarks[handNo]
            
            # for id,lm in enumerate(handLandMarks.landmark[handNo]):
            for id,lm in enumerate(myHand.landmark):
                
                
                print(id,lm)
                h,w,c=frame.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),15,(125,0,125),cv2.FILLED)
        return lmList

    def labelHands(self,frame,myHands,handsType,draw=True):
        for hand,handType in zip(myHands,handsType):
            if handType=='Right':
                lbl='Right'
                print('this is my ',lbl)
                # cv2.putText(frame,lbl,hand[8],cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
        for hand,handType in zip(myHands,handsType):        
            if handType=='Left':
                lbl='Left'
                print('this is my ',lbl)
                print(hand[8])
            if draw:
                cv2.putText(frame,lbl,hand[8],cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
def main():
    import cv2
    print(cv2.__version__)
    import time 
    width=1280
    height=720
    cam=cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
    cam.set(cv2.CAP_PROP_FPS, 30)
    cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
    
    findHands=mpHands(2)
    # findFace=mpFace()
    # findPose=mpPose()
    print(findHands.__dict__)
    font=cv2.FONT_HERSHEY_SIMPLEX
    fontColor=(0,0,255)
    pTime=0
    cTime=0
    while True:
        ignore,  frame = cam.read()
        frame=cv2.resize(frame,(width,height))
        frame=cv2.flip(frame,1)
        frame,handsLM,handsType=findHands.Marks(frame,True)
        lmList=findHands.findPosition(frame,0,True)
        findHands.labelHands(frame,handsLM,handsType)
        
        # faceLoc=findFace.Marks(frame)
        # poseLM=findPose.Marks(frame)
        print(handsType)
        if len(lmList)!=0:
                # print(lmList[4])
                id,x,y=lmList[4]
                # print(x,' ',y,' ',id)
                cv2.circle(frame,(x,y),20,(255,255,0),2)
        
        
        
        # print(findPose.__dict__)
        # if poseLM != []:
        #     for ind in [13,14,15,16]:
        #         cv2.circle(frame,poseLM[ind],20,(0,255,0),-1)
                
        #     for ind in [19]:
        #         cv2.circle(frame,poseLM[ind],20,(0,255,255),-1)
                # print(poseLM[19])
    
        # for face in faceLoc:
        #     cv2.rectangle(frame,face[0],face[1],(255,0,0),3)
        # for hand,handType in zip(handsLM,handsType):
        #     if handType=='Right':
        #         lbl='Right'
        #     if handType=='Left':
        #         print(hand[8])
        #         lbl='Left'

        #     cv2.putText(frame,lbl,hand[8],font,2,fontColor,2)
            
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
        cv2.imshow('my WEBcam', frame)
        cv2.moveWindow('my WEBcam',0,0)
        if cv2.waitKey(1) & 0xff ==ord('q'):
            break
    cam.release()
if __name__=='__main__':
    main()