'''THis is the FingerCount_1.py  modified with the parsing placed in a function to return a vlaue to be sent to the picoW
basic five finger count
import handTrackModule as ht
from htm import mpHands
myObject=htm()
frame,myHands,handsType=myObject.Marks(frame,draw=False)
all_lmLists=myObject.findPostions(frame,draw=False)
right_hand_coords, left_hand_coords   =myObject.labelHands(self, frame, myHands, handsType, draw=True)

'''
# import cv2
# import time
# import os
# import handTrackModule as ht


# wCam, hCam = 1280, 760
# cap = cv2.VideoCapture(1)
# cap.set(3, wCam)
# cap.set(4, hCam)
# folderPath = "/Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/Images/FingerCount"
# # folderPath = "/Images/FingerImages"
# # myList = os.listdir(folderPath)
# # print(myList)
# myList=['a6.png','a1.png', 'a2.png', 'a3.png', 'a4.png', 'a5.png']
# print(myList)

# overlayList = []
# for imPath in myList:
#     image = cv2.imread(f'{folderPath}/{imPath}')
#     image=cv2.resize(image,(360,480))
#     # print(f'{folderPath}/{imPath}')
#     overlayList.append(image)
# # print(len(overlayList))
# # print(overlayList[0])
# # print("image  ",image.shape)
# pTime = 0
# detector=ht.mpHands(2,.75,.75)
# # detector = ht.handDetector(.75,.75)
# tipIds = [4, 8, 12, 16, 20]## instead of a bunch of if conditions we will use a for loop of these finger tips
# def counter_fingers(img):
#     img,myHands,handsType = detector.Marks(img)
#     all_lmLists=detector.findPositions(img,draw=False)
  
#     if len(all_lmLists)!=0:
#         fingers=[]
#         print(all_lmLists)
#         for handType,Lists in zip(handsType,all_lmLists):
#             print(handType,Lists)
#             if handType=='Right':
#                 print('Right',handType)
#                 if ( Lists[tipIds[0]][1]<Lists[tipIds[0]-1][1] ):## this is to adress the thumb!! for the right hand
#                     fingers.append(1)
#                 else:
#                     fingers.append(0)
#                 print(fingers)
#             if handType=='Left':
#                 print('Left',handType)
#                 if ( Lists[tipIds[0]][1]>Lists[tipIds[0]-1][1] ):## this is to adress the thumb!! for the right hand
#                     fingers.append(1)
#                 else:
#                     fingers.append(0)
#                 print(fingers)
      
#             for id in range(1,len(tipIds),1):##This was ' for id in range(0,len(tipIds)' but because of the thumb will decrease it by one and create a codniton just for the thumb, and start at index 1 not zero!!!!!!!!!!!
#                 if Lists[tipIds[id]][2]<Lists[tipIds[id]-2][2]:
#                     fingers.append(1)
#                 else:
#                     fingers.append(0)
#             print(fingers)
#             print(fingers.count(1))## this counts the number of ones
#             totalFingers=fingers.count(1)
#             RealTotal=totalFingers
#             if totalFingers>=5:
#                 totalFingers=5
#             # print(fingers.count(0))
#             h,w,c =overlayList[totalFingers].shape
#             # print(h,w,c)
#             img[0:int(h),0:int(w)]=overlayList[totalFingers]
#         cv2.rectangle(img, (20, hCam-40), (240, hCam-200), (0, 255, 0), cv2.FILLED)
#         cv2.putText(img, str(RealTotal), (45, hCam-80), cv2.FONT_HERSHEY_PLAIN,
#                     10, (255, 0, 0), 25)
#         return  fingers.count(1)




# while True:
#     success, img = cap.read()
#     img=cv2.flip(img,1)
 
#     RealTotal=counter_fingers(img)
#     print('returned value',RealTotal)
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
#     cv2.imshow("Image", img)
#     if cv2.waitKey(1)&0xff==27:
#         break
# cap.release()

# cv2.destroyAllWindows()
###~~~~~ create socket client sending gthe total number of fingers

import cv2
import time
import os
import handTrackModule as ht
import socket
# Setup socket connection
# HOST = '0.0.0.0'  # Replace with Raspberry Pi Pico's IP
# PORT = 12345

HOST = '192.168.1.30'  # Use the Pico W AP IP address
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
## start videiCam
wCam, hCam = 1280, 760
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
#/Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/Images/FingerCount
folderPath = "/Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/Images/FingerCount"
# folderPath = "/Images/FingerImages"
# myList = os.listdir(folderPath)
# print(myList)
myList=['a6.png','a1.png', 'a2.png', 'a3.png', 'a4.png', 'a5.png']
print(myList)

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
def counter_fingers(img):
    img,myHands,handsType = detector.Marks(img)
    all_lmLists=detector.findPositions(img,draw=False)
  
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
      
            for id in range(1,len(tipIds),1):##This was ' for id in range(0,len(tipIds)' but because of the thumb will decrease it by one and create a codniton just for the thumb, and start at index 1 not zero!!!!!!!!!!!
                if Lists[tipIds[id]][2]<Lists[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            print(fingers)
            print(fingers.count(1))## this counts the number of ones
            totalFingers=fingers.count(1)
            RealTotal=totalFingers or 0
            if RealTotal is None:
                print("No fingers detected")
            else:
                print(f'Sending Total Fingers: {RealTotal}')

            if totalFingers>=5:
                totalFingers=5
            # print(fingers.count(0))
            h,w,c =overlayList[totalFingers].shape
            # print(h,w,c)
            img[0:int(h),0:int(w)]=overlayList[totalFingers]
        cv2.rectangle(img, (20, hCam-40), (240, hCam-200), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(RealTotal), (45, hCam-80), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
        return  fingers.count(1)




while True:
    success, img = cap.read()
    if not success:
        break
    img=cv2.flip(img,1)
 
    # RealTotal=counter_fingers(img)
    # print(f'Sending Total Fingers: {RealTotal}')
    
    # Send finger count as a string
 

    try:
        RealTotal = counter_fingers(img) or 0
        print(f'Sending Total Fingers: {RealTotal}')
        
        # client_socket.sendall(str(RealTotal).encode())
        client_socket.sendall(f'{RealTotal}\n'.encode())
    except (BrokenPipeError, ConnectionResetError):
        print("Connection lost! Trying to reconnect...")
        client_socket.close()
        time.sleep(2)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1)&0xff==27:
        break
cap.release()
client_socket.close()

cv2.destroyAllWindows()