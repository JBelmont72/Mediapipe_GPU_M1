'''
path to the module in .venv  /Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/.venv/lib/python3.11/site-packages/mediapipe/python/solutions/face_detection.py
min_detection_confidence=0.5, model_selection=0
set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))


class FaceDetection(SolutionBase):
  """MediaPipe Face Detection.

  MediaPipe Face Detection processes an RGB image and returns a list of the
  detected face location data.

  Please refer to
  https://solutions.mediapipe.dev/face_detection#python-solution-api
  for usage examples.
  """

  def __init__(self, min_detection_confidence=0.5, model_selection=0):
    """Initializes a MediaPipe Face Detection object.

    Args:
      min_detection_confidence: Minimum confidence value ([0.0, 1.0]) for face
        detection to be considered successful. See details in
        https://solutions.mediapipe.dev/face_detection#min_detection_confidence.
      model_selection: 0 or 1. 0 to select a short-range model that works
        best for faces within 2 meters from the camera, and 1 for a full-range
        model best for faces within 5 meters. See details in
        https://solutions.mediapipe.dev/face_detection#model_selection.
    """
    output of detection in enumerate results.detections     :
0 label_id: 0
score: 0.53910613
location_data {
  format: RELATIVE_BOUNDING_BOX
  relative_bounding_box {
    xmin: 0.3473559
    ymin: 0.18022256
    width: 0.25629103
    height: 0.14416297
  }
  relative_keypoints {
    x: 0.45510793
    y: 0.22188681
  }
  relative_keypoints {
    x: 0.5320685
'''
import cv2
import mediapipe as mp
import time
# cap=cv2.VideoCapture(1)
# cap=cv2.VideoCapture('Images/Erica.mov')
cap=cv2.VideoCapture('Images/MiriamTap.mov')
width =1280
height= 720
# cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourrc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cap.set(cv2.CAP_PROP_FPS,30)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
cTime=0
pTime=0
mpFaceDetection=mp.solutions.face_detection # imports the face_detection module
mpDraw = mp.solutions.drawing_utils ## for this to draw use: mpDraw.draw_detection(img,detection)
faceDetection=mpFaceDetection.FaceDetection(min_detection_confidence=0.3, model_selection=1)
while True:
    ret,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=faceDetection.process(imgRGB)
    if results.detections != None:
        # location_data = results.detections[0].location_data
        for id,detection in enumerate(results.detections):
            # mpDraw.draw_detection(img,detection)
            # print(id,detection)
            # print(f'LOCATION DATA: {detection.location_data}')
            # print('score', detection.score)
            score=int(detection.score[0]*100)
            print(score)
            # print('location_data: ',detection.location_data.relative_bounding_box)
            # print(detection.location_data.relative_bounding_box.xmin)
            # ymin=detection.location_data.relative_bounding_box.ymin
            # print(detection.location_data.relative_bounding_box)
            bbox=detection.location_data.relative_bounding_box
            ih,iw,ic = img.shape
            x1=int(bbox.xmin*iw)
            y1=int(bbox.ymin*ih)
            x2=int((bbox.xmin+bbox.width)*iw)
            y2=int((bbox.ymin+bbox.height)*ih)
            # cv2.rectangle(img,(30,80),(140,135),(255,255,255),-1)
            cv2.putText(img,f'{str(score)}%',(x1,y1-20),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
            print((int(bbox.xmin*iw),(int(bbox.ymin*ih))), (int((bbox.xmin+bbox.width)*iw),int((bbox.ymin+bbox.height)*ih)))
            cv2.rectangle(img,(int(bbox.xmin*iw),(int(bbox.ymin*ih))), (int((bbox.xmin+bbox.width)*iw),int((bbox.ymin+bbox.height)*ih)),(255,0,255),3)
            # cv2.circle(img,(int((x1+x2)/2),int((y1+y2)/2)),30,(0,0,255),4)
       
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    FPS=str(int(24*.80+fps*0.20))
    cv2.rectangle(img,(18,25),(200,75),(0,250,250),-1)
    cv2.putText(img,f'{FPS}fps',(25,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),2)
    cv2.imshow('Image',img)
    if cv2.waitKey(1)& 0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()