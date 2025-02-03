
'''Finger count 
the third program is my work through on the problem. Lots of important steps


The os.listdir() method in Python is used to get the list of all files and directories in the specified directory. If we don’t specify any directory, then a list of files and directories in the current working directory will be returned.
'''

# import cv2
# import time
# import os
# import handTrackModule as htm
# wCam, hCam = 640, 480
# cap = cv2.VideoCapture(1)
# wCam=640

# hCam=480
# cap.set(3, wCam)
# cap.set(4, hCam)
# myList=['a6.png','a1.png', 'a2.png', 'a3.png', 'a4.png', 'a5.png']

# folderPath = "/Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/Images/FingerCount"
# # myList = os.listdir(folderPath)
# print(myList)
# overlayList = []
# for imPath in myList:
#     # image=cv2.imread(imPath)
#     image = cv2.imread(f'{folderPath}/{imPath}')
#     image=cv2.resize(image,(640,480))
#     print(f'{folderPath}/{imPath}')
#     overlayList.append(image)
# print(len(overlayList))
# pTime = 0
# detector = htm.handDetector()
# tipIds = [4, 8, 12, 16, 20]
# while True:
#     success, img = cap.read()
    
#     img = detector.findHands(img)
#     print(img.shape)
#     lmList = detector.findPosition(img, draw=False)
#     print(lmList)
#     # print(lmList)
#     if len(lmList) != 0:
#         fingers = []
#         # Thumb
#         if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]: # if the tipId is greater than the first one(thumb tip is tip 4 but tipId 0, THEN append)
#             # print(f'\n\ttipIDs:  {tipIds}\n {lmList[tipIds[0]][1]} ipIds[0] - 1][1] {lmList[tipIds[0] - 1][1]}')
#             fingers.append(1)
#         else:
#             fingers.append(0)       ## but if it is tipID 0 (the thumb) go ahead and append
#         # 4 Fingers
#         print('fingers: ',fingers) ## it is [1]  except when a thumb
#         for id in range(1, 5):
#             if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
#                 fingers.append(1)
#             else:
#                 fingers.append(0)### note the here we are adding the number 1 or zero if the finger ids show
#         # print(fingers)
#         totalFingers = fingers.count(1)
#         print(totalFingers)
#         h, w, c = overlayList[totalFingers].shape
#         print('h, w, c   ', h, w, c)
#         img[0:h, 0:w] = overlayList[totalFingers]
#         cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
#         cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
#                     10, (255, 0, 0), 25)
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
#                 3, (255, 0, 0), 3)
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)

## this works /Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/Images/FingerImages
# import cv2
# import time
# import os
# import handTrackModule as ht


# wCam, hCam = 640, 480
# cap = cv2.VideoCapture(1)
# cap.set(3, wCam)
# cap.set(4, hCam)
# folderPath = "/Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/Images/FingerCount"
# # folderPath = "/Images/FingerImages"
# myList = os.listdir(folderPath)
# # i used this to get the order of images straight:
# myList=['a6.png','a1.png', 'a2.png', 'a3.png', 'a4.png', 'a5.png']
# print(myList)

# overlayList = []
# for imPath in myList:
#     image = cv2.imread(f'{folderPath}/{imPath}')
#     image=cv2.resize(image,(360,480))
#     # print(f'{folderPath}/{imPath}')
#     overlayList.append(image)
# print(len(overlayList))
# pTime = 0
# detector = ht.handDetector(.5,.75)
# tipIds = [4, 8, 12, 16, 20]

# while True:
#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList = detector.findPosition(img, draw=False)
#     # print(lmList)
#     if len(lmList) != 0:
#         fingers = []
#         # Thumb
#         if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
#             fingers.append(1)
#         else:
#             fingers.append(0)
#         # 4 Fingers
#         for id in range(1, 5):
#             if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
#                 fingers.append(1)
#             else:
#                 fingers.append(0)
#         print(fingers)
#         totalFingers = fingers.count(1)
#         print(totalFingers)
        
#         h, w, c = overlayList[totalFingers].shape
#         img[0:h, 0:w] = overlayList[totalFingers]
        
#         # h, w, c = overlayList[totalFingers - 1].shape
#         # img[0:h, 0:w] = overlayList[totalFingers - 1]
#         cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
#         cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
#                     10, (255, 0, 0), 25)
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
#                 3, (255, 0, 0), 3)
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)
#############work file
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
import os 

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
detector = ht.handDetector(.75,.75)
tipIds = [4, 8, 12, 16, 20]## instead of a bunch of if conditions we will use a for loop of these finger tips
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    # print('img  ',img.shape)
    ## if len(lmList)!= 0:     ## lmList[6][2] this is the 6 landmark and the third element of the tuple which is the y value
        ## if lmList[6][2]< lmList[4][2]:## compares the tip and base y values of the index finger
        ##     print("the index finger is up")
    ## the thumb is a problem because the thumb never goes below the base!!!!
    ## can chekc if the thumb is to the left or right of the base
    
    ## because of the thumbthis is written for the right hand (later I can add a handedness conditon )
    
    if len(lmList)!=0:
        fingers=[]
        
        # if ( lmList[tipIds[0]][2]>lmList[tipIds[0]-1][2] )or ( lmList[tipIds[0]][1]>lmList[tipIds[0]-2][2] ):## this is to adress the thumb!! for the right hand
        ## below is for the left hand and i used the index one of lmList which is the x value.(for the othe rfingers used the y value)
        if ( lmList[tipIds[0]][1]<lmList[tipIds[0]-1][1] ):## this is to adress the thumb!! for the right hand
            fingers.append(1)
        else:
            fingers.append(0)
        
        
        
        
        
        for id in range(1,len(tipIds),1):##This was ' for id in range(0,len(tipIds)' but because of the thumb will decrease it by one and create a codniton just for the thumb, and start at index 1 not zero!!!!!!!!!!!
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        # print(fingers.count(1))## this counts the number of ones
        totalFingers=fingers.count(1)
        # print(fingers.count(0))
        h,w,c =overlayList[totalFingers].shape
        # print(h,w,c)
        img[0:int(h),0:int(w)]=overlayList[totalFingers]
    
    
    
    
    
    # if len(lmList) != 0:
    #     fingers = []
    #     # Thumb
    #     if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
    #         fingers.append(1)
    #     else:
    #         fingers.append(0)
    #     # 4 Fingers
    #     for id in range(1, 5):
    #         if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
    #             fingers.append(1)
    #         else:
    #             fingers.append(0)
    #     # print(fingers)
    #     totalFingers = fingers.count(1)
    #     print(totalFingers)
    #     h, w, c = overlayList[totalFingers - 1].shape
    #     img[0:h, 0:w] = overlayList[totalFingers - 1]
        cv2.rectangle(img, (20, hCam-40), (170, hCam-200), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, hCam-80), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1)&0xff==27:
        break
cap.release()

cv2.destroyAllWindows()