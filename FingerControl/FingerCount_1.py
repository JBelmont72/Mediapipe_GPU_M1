'''
basic five finger count
import handTrackModule as ht
from htm import mpHands
myObject=htm()
frame,myHands,handsType=myObject.Marks(frame,draw=False)
all_lmLists=myObject.findPostions(frame,draw=False)
right_hand_coords, left_hand_coords   =myObject.labelHands(self, frame, myHands, handsType, draw=True)

'''
import cv2
import time
import os
import handTrackModule as ht


wCam, hCam = 1280, 760
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
folderPath = "/Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/Images/FingerCount"
# folderPath = "/Images/FingerImages"
# myList = os.listdir(folderPath)
# print(myList)
myList=['a6.png','a1.png', 'a2.png', 'a3.png', 'a4.png', 'a5.png']
print(myList)
# # importing os module  Experimented with os.listdir(path)
# import os 

# # Get the list of all files and directories 
# path = "/Library/Scripts/"
# dir_list = os.listdir(path) 

# print("Files and directories in '", path, "' :") 

# # print the list 
# print('DIR_LIST/Library/Scripts:    ',dir_list)
# path = os.getcwd() 
   
# # Get the list of all files and directories 
# dir_list = os.listdir(path) 
   
# print("Files and directories in '", path, "' :")  
# # print the list 
# print(dir_list)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    image=cv2.resize(image,(360,480))
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))
# print(overlayList[0])
# print("image  ",image.shape)
pTime = 0
detector=ht.mpHands(2,.75,.75)
# detector = ht.handDetector(.75,.75)
tipIds = [4, 8, 12, 16, 20]## instead of a bunch of if conditions we will use a for loop of these finger tips
while True:
    success, img = cap.read()
    img=cv2.flip(img,1)
    img,myHands,handsType = detector.Marks(img)
    all_lmLists=detector.findPositions(img,draw=False)
    # lmList = detector.findPosition(img, draw=False)
    
    # print(lmList)
    # print('img  ',img.shape)
    ## if len(lmList)!= 0:     ## lmList[6][2] this is the 6 landmark and the third element of the tuple which is the y value
        ## if lmList[6][2]< lmList[4][2]:## compares the tip and base y values of the index finger
        ##     print("the index finger is up")
    ## the thumb is a problem because the thumb never goes below the base!!!!
    ## can chekc if the thumb is to the left or right of the base
    
    ## because of the thumb,this is written for the right hand (later I can add a handedness conditon )
    
    if len(all_lmLists)!=0:
        fingers=[]
        print(all_lmLists)
        for handType,Lists in zip(handsType,all_lmLists):
            print(handType,Lists)
            if handType=='Right':
                print('Right',handType)
                if ( Lists[tipIds[0]][1]<Lists[tipIds[0]-1][1] ):## this is to adress the thumb!! for the right hand
                    fingers.append(1)
                else:
                    fingers.append(0)
                print(fingers)
            if handType=='Left':
                print('Left',handType)
                if ( Lists[tipIds[0]][1]>Lists[tipIds[0]-1][1] ):## this is to adress the thumb!! for the right hand
                    fingers.append(1)
                else:
                    fingers.append(0)
                print(fingers)

                # if ( Lists[tipIds[0]][2]>Lists[tipIds[0]-1][2] )or ( Lists[tipIds[0]][1]>Lists[tipIds[0]-2][2] ):## this is to adress the thumb!! for the right hand
                # # below is for the left hand and i used the index one of lmList which is the x value.(for the othe rfingers used the y value)
        
                # # if ( all_lmLists[tipIds[0]][1]<all_lmLists[tipIds[0]-1][1] ):## this is to adress the thumb!! for the right hand
                #     fingers.append(1)
                # else:
                #     fingers.append(0)
        
                # print(fingers)
        
        
            
            for id in range(1,len(tipIds),1):##This was ' for id in range(0,len(tipIds)' but because of the thumb will decrease it by one and create a codniton just for the thumb, and start at index 1 not zero!!!!!!!!!!!
                if Lists[tipIds[id]][2]<Lists[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            print(fingers)
            print(fingers.count(1))## this counts the number of ones
            totalFingers=fingers.count(1)
            RealTotal=totalFingers
            if totalFingers>=5:
                totalFingers=5
            # print(fingers.count(0))
            h,w,c =overlayList[totalFingers].shape
            # print(h,w,c)
            img[0:int(h),0:int(w)]=overlayList[totalFingers]
            

    
    
    
    # # if len(lmList) != 0:
    # #     fingers = []
    # #     # Thumb
    # #     if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
    # #         fingers.append(1)
    # #     else:
    # #         fingers.append(0)
    # #     # 4 Fingers
    # #     for id in range(1, 5):
    # #         if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
    # #             fingers.append(1)
    # #         else:
    # #             fingers.append(0)
    # #     # print(fingers)
    # #     totalFingers = fingers.count(1)
    # #     print(totalFingers)
    # #     h, w, c = overlayList[totalFingers - 1].shape
    # #     img[0:h, 0:w] = overlayList[totalFingers - 1]
        cv2.rectangle(img, (20, hCam-40), (240, hCam-200), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(RealTotal), (45, hCam-80), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1)&0xff==27:
        break
cap.release()

cv2.destroyAllWindows()