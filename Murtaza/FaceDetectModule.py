'''

'''
import cv2
import mediapipe as mp
import time

class mpFaceDetect():
    def __init__(self,min_detection_confidence=0.3, model_selection=1):
        self.min_detection_confidence=min_detection_confidence
        self.model_selection=model_selection
        self.mpFaceDetection=mp.solutions.face_detection # imports the face_detection module
        self.mpDraw = mp.solutions.drawing_utils ## for this to draw use: mpDraw.draw_detection(img,detection)
        self.faceDetection=self.mpFaceDetection.FaceDetection(self.min_detection_confidence, self.model_selection)
    def mpFaceProcess(self,img):
            imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            results=self.faceDetection.process(imgRGB)
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




def main():
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
    myFaceDetect=mpFaceDetect()
    while True:
        ret,img=cap.read()
        myFaceDetect.mpFaceProcess(img)
        cTime=0
        pTime=0       
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




if  __name__=='__main__':
    main()
 