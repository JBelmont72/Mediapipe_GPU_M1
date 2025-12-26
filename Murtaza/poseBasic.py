'''
https://github.com/freeCodeCamp/freeCodeCamp

path to the mediapipe library for POSE:  /Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/.venv/lib/python3.11/site-packages/mediapipe/python/solutions/pose.py

def process(self, image: np.ndarray) -> NamedTuple:
    """Processes an RGB image and returns the pose landmarks on the most prominent person detected.

    Args:
      image: An RGB image represented as a numpy ndarray.

    Raises:
      RuntimeError: If the underlying graph throws any error.
      ValueError: If the input image is not three channel RGB.

    Returns:
      A NamedTuple with fields describing the landmarks on the most prominate
      person detected:
        1) "pose_landmarks" field that contains the pose landmarks.
        2) "pose_world_landmarks" field that contains the pose landmarks in
        real-world 3D coordinates that are in meters with the origin at the
        center between hips.
        3) "segmentation_mask" field that contains the segmentation mask if
           "enable_segmentation" is set to true.

results = super().process(input_data={'image': image})
    if results.pose_landmarks:  # pytype: disable=attribute-error
      for landmark in results.pose_landmarks.landmark:  # pytype: disable=attribute-error
        landmark.ClearField('presence')
    if results.pose_world_landmarks:  # pytype: disable=attribute-error
      for landmark in results.pose_world_landmarks.landmark:  # pytype: disable=attribute-error
        landmark.ClearField('presence')
    return results


def __init__(self,static_image_mode=False, model_complexity=1, smooth_landmarks=True, enable_segmentation=False,
                smooth_segmentation=True, min_detection_confidence=0.5, min_tracking_confidence=0.5):
make sure to pass those to self.pose

static_mode_mode  if False, the detection is used once and then just use tracking until the conficence level is too low,  if this hppens then it goes back to capture again
https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/pose.md

pose is the OBJECT!, pose=mpPose() is where it is instantiated!! 

and mpPose is where the object is inserted into the solutions method
.venv/lib/python3.11/site-packages/mediapipe/python/solutions/pose.py
this is where the Pose class is located

pose = mpPose(mp.solutions.pose).Pose(parameters)
'''
import cv2
import mediapipe as mp ## uses bgr
import time
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose ### we create this to enable instantiation of pose in the next line
pose = mpPose.Pose(static_image_mode=False,         # the pose object is instantiated
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
    smooth_landmarks=True)
# cap = cv2.VideoCapture('PoseVideos/3.mp4')
cap = cv2.VideoCapture('Images/PoseVid_1.mov')
pTime = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks) ## the .pose_landmarks  takes us into the data structure of 'results'
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            # print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y * h)
            print([id,cx,cy])
            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED) 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.rectangle(img,(60,15),(140,60),(125,125,0),-1)
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    
