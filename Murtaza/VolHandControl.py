'''The first uses the handTrackModule.py  which does not have the unnecessary (for this script)returning of handtypes and hand landlamrks
The second runs much slower because it it doing extra processing all the time and is using the HandModule.py
applescript https://www.youtube.com/watch?v=IGiGTKrszz4
this is a good tutorial for creating applescriopts to do tasks  which are like mini applications
'''
import cv2
import time
import numpy as np
import handTrackModule as htm
import math
# from ctypes import cast, POINTER
'''
https://dev.to/0xkoji/control-mac-sound-volume-by-python-h4g
TO SET VOLUME:
import osascript
target_volume = 50
vol = "set volume output volume " + str(50)
osascript.osascript(vol)

# or
target_volume = 50
osascript.osascript("set volume output volume {}".format(target_volume))

# or
osascript.osascript("set volume output volume 50")


Get volume info
The return format is and what we need is output volume to know the current sound volume.

(0, 'output volume:50, input volume:58, alert volume:100, output muted:false', '')
The way to get the current volume is straightforward.
Get the volume settings via osascript and parse the tuple.

result = osascript.osascript('get volume settings')
print(result)
print(type(result))
volInfo = result[1].split(',')
outputVol = volInfo[0].replace('output volume:', '')
print(outputVol)
The result is 50.
'''

################################
wCam, hCam = 640, 480
################################
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector()
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
# volRange = volume.GetVolumeRange()
# minVol = volRange[0]
# maxVol = volRange[1]
import osascript
# target_volume = 50
# osascript.osascript("set volume output volume {}".format(target_volume))


minVol = 0
maxVol = 100
vol = 0
volBar = 400
volPer = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)
        # Hand range 50 - 300
        # Volume Range -65 - 0
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length), vol)
        osascript.osascript("set volume output volume {}".format(vol))
        # volume.SetMasterVolumeLevel(vol, None)
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)
    #######~~~~~~~~~~~~
# import osascript
# import cv2
# import time
# import numpy as np
# import HandModule as htm
# # import handTrackModule as htm
# import math
# # from ctypes import cast, POINTER
# ################################
# wCam, hCam = 640, 480
# ################################
# cap = cv2.VideoCapture(1)
# cap.set(3, wCam)
# cap.set(4, hCam)
# pTime = 0
# # detector = htm.handDetector()
# detector = htm.mpHands()

# # minVol = volRange[0]
# # maxVol = volRange[1]
# import osascript
# # target_volume = 50
# # osascript.osascript("set volume output volume {}".format(target_volume))
# minVol = 0
# maxVol = 100
# vol = 0
# volBar = 400
# volPer = 0
# while True:
#     success, img = cap.read()
#     frame,myHands,handsType = detector.Marks(img,True)
#     lmList = detector.findPosition(img, draw=False)
#     if len(lmList) != 0:
#         # print(lmList[4], lmList[8])
#         x1, y1 = lmList[4][1], lmList[4][2]
#         print(x1,y1)
        
#     osascript.osascript("set volume output volume {}".format(vol))
#         # volume.SetMasterVolumeLevel(vol, None)
#     # if length < 50:
#     #     cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
#     cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
#     cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
#     cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
#                 1, (255, 0, 0), 3)
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
#                 1, (255, 0, 0), 3)
#     cv2.imshow("Img", img)
#     cv2.waitKey(1)