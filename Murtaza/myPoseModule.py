'''
min_detection_confidence=0.7,
min_tracking_confidence=0.7
additional parmeters for self.Pose
enable_segmentation

If set to true, in addition to the pose landmarks the solution also generates the segmentation mask. Default to false.

smooth_segmentation

If set to true, the solution filters segmentation masks across different input images to reduce jitter. Ignored if enable_segmentation is false or static_image_mode is true. Default to true.

'''

# import cv2
# import mediapipe as mp ## uses bgr
# import time
# class mpPose():
#     def __init__(self,static_image=False ,min_detection_confidence=0.7,
# min_tracking_confidence=0.7):
#         self.mpDraw = mp.solutions.drawing_utils
#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose()

#     def poseDetector(self,img):
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = self.pose.process(imgRGB)
#         # print(results.pose_landmarks)
#         if results.pose_landmarks:
#             self.mpDraw.draw_landmarks(img, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
#             for id, lm in enumerate(results.pose_landmarks.landmark):
#                 h, w, c = img.shape
#                 # print(id, lm)
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 # print([id,cx,cy])
#                 cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
#         return img


# def main():
#     cap = cv2.VideoCapture('Images/PoseVid_1.mov')
#     pTime = 0
#     myPose=mpPose()
#     while True:
#         success, img = cap.read()
#         img=myPose.poseDetector(img)
#         # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         # results = pose.process(imgRGB)
#         # # print(results.pose_landmarks)
#         # if results.pose_landmarks:
#         #     mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
#         #     for id, lm in enumerate(results.pose_landmarks.landmark):
#         #         h, w, c = img.shape
#         #         # print(id, lm)
#         #         cx, cy = int(lm.x * w), int(lm.y * h)
#         #         # print([id,cx,cy])
#         #         cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#         cv2.rectangle(img,(60,15),(140,60),(125,125,0),-1)
#         cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
#                     (255, 0, 0), 3)
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)




# if __name__ == '__main__':
#     main()

# mp_pose = mp.solutions.pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
# mp_drawing = mp.solutions.drawing_utils
# cap = cv2.VideoCapture('video_path')

## solutions.pose.Pose()
'''
self,
               static_image_mode=False,
               model_complexity=1,
               smooth_landmarks=True,
               enable_segmentation=False,
               smooth_segmentation=True,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):

'''
import cv2
# import mediapipe as mp ## uses bgr
import time
import mediapipe as mp
class mpPose():
    def __init__(self,static_image_mode=False ,model_complexity=1,min_detection_confidence=0.5,
               min_tracking_confidence=0.5):  
        self.static_image_mode=static_image_mode 
        self.model_complexity=model_complexity
        self.min_detection_confidence=min_detection_confidence
        self.min_tracking_confidence=min_tracking_confidence
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose=self.mpPose.Pose(self.static_image_mode,self.model_complexity,self.min_detection_confidence)
        # self.pose = self.mpPose.Pose(self.mode,
        #     self.static_image, 
        #     self.min_detection_confidence,
        #     self.smooth_landmarks,
        #     self.enable_segmentation,
            
        #     self.min_tracking_confidence,
        #     self.model_complexity)
    def poseDetector(self,img,draw=False,flag=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(imgRGB)
        if results.pose_landmarks:
            self.mpDraw.draw_landmarks(img, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            # self.mpDraw.draw_landmarks(img, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            # print(results.pose_landmarks) 
            poseLandmarks=[]
            poseIndex=[]
            # for id,ldMk in enumerate(results.pose_landmarks.landmark):
            #     print(f'for index {id} the values are {ldMk.x,ldMk.y}.')
            # print(results.pose_landmarks.landmark)        
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                poseIndex.append(id)
                poseLandmarks.append([cx,cy])
            # print(poseIndex)
            # print(poseLandmarks)      
            if draw:
                self.mpDraw.draw_landmarks(
                img, 
                results.pose_landmarks, 
                mp.solutions.pose.POSE_CONNECTIONS,
                self.mpDraw.DrawingSpec(color=(255, 0, 0), thickness=0, circle_radius=6),
                self.mpDraw.DrawingSpec(color=(255, 0, 0), thickness=6, circle_radius=0) ) ## the first is circle radius and second is line thickness
            if flag:     
                # print([id,cx,cy])
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return poseIndex, poseLandmarks
def main():
    cap = cv2.VideoCapture('Images/PoseVid_1.mov')
    pTime = 0
    myPose=mpPose()
    while True:
        success, img = cap.read()
        poseIndex,poseLandmarks=     myPose.poseDetector(img,draw=True,flag=False)
        # print(poseIndex,poseLandmarks)
        # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # results = pose.process(imgRGB)
        # # print(results.pose_landmarks)
        # if results.pose_landmarks:
        #     mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        #     for id, lm in enumerate(results.pose_landmarks.landmark):
        #         h, w, c = img.shape
        #         # print(id, lm)
        #         cx, cy = int(lm.x * w), int(lm.y * h)
        #         # print([id,cx,cy])
        #         cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)       
        if poseIndex!=None:
            for i in range(10,20,2):
                x=poseLandmarks[i]
                cv2.circle(img,x,25,(255,255,0),-1) 
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.rectangle(img,(60,15),(140,60),(125,125,0),-1)
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1) 
if __name__ == '__main__':
    main()
    
    
