'''
my practice new detect module  as of 1 Feb 2025, same as  the 'FaceDetectModule.py

'''
import cv2
import mediapipe as mp
import time

class mpFaceDetect():
    def __init__(self,min_detection_confidence=0.3, model_selection=1):
        # self.width =640
        # self.height= 360
        self.width =1280
        self.height= 720
        self.min_detection_confidence=min_detection_confidence
        self.model_selection=model_selection
        self.mpFaceDetection=mp.solutions.face_detection # imports the face_detection module
        self.mpDraw = mp.solutions.drawing_utils ## for this to draw use: mpDraw.draw_detection(img,detection)
        self.faceDetection=self.mpFaceDetection.FaceDetection(self.min_detection_confidence, self.model_selection)
    def mpFaceProcess(self,img,draw=False,flip=True):
        if flip:
            img=cv2.flip(img,1)
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results=self.faceDetection.process(imgRGB)
        bboxs=[]
        if results.detections != None:
    # location_data = results.detections[0].location_data
            for id,detection in enumerate(results.detections):
                # mpDraw.draw_detection(img,detection)
                # print(id,detection)
                # print(f'LOCATION DATA: {detection.location_data}')
                # print('score', detection.score)
                score=int(detection.score[0]*100)
                # print(score)
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
                # bBox=int(bbox.xmin*iw),(int(bbox.ymin*ih)), int((bbox.width)*iw),int((bbox.height)*ih) 
                bBox=(int(bbox.xmin*iw),(int(bbox.ymin*ih))), (int((bbox.xmin+bbox.width)*iw),int((bbox.ymin+bbox.height)*ih))## this gave me the actual values for the box
                bboxs.append([id,bBox,score])
                if draw:
                    img=self.fancyDraw(img,bBox)
                
                # cv2.rectangle(img,(30,80),(140,135),(255,255,255),-1)
                    cv2.putText(img,f'{str(score)}%',(x1,y1-20),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
                # print((int(bbox.xmin*iw),(int(bbox.ymin*ih))), (int((bbox.xmin+bbox.width)*iw),int((bbox.ymin+bbox.height)*ih)))
                cv2.rectangle(img,bBox[0],bBox[1],(255,0,255),2)## works
                # cv2.rectangle(img,(int(bbox.xmin*iw),(int(bbox.ymin*ih))), (int((bbox.xmin+bbox.width)*iw),int((bbox.ymin+bbox.height)*ih)),(255,0,255),3)
                # cv2.circle(img,(int((x1+x2)/2),int((y1+y2)/2)),30,(0,0,255),4)
                
        return  img,bboxs
    def fancyDraw(self,img,bBox,l=30,t=14,rt=1,color=(255,0,255)):## will send one bounding box at a time
        pnt1,pnt2=bBox
        x1,y1=pnt1
        x2,y2=pnt2
        cv2.line(img,pnt1,(pnt1[0]+l,pnt1[1]),(255,0,255),t)
        cv2.line(img,pnt1,(pnt1[0],pnt1[1]+l),(255,0,255),t)
        cv2.rectangle(img,bBox[0],bBox[1],(255,0,255),rt)
        ## top right
        cv2.line(img,(x2-l,y1),(x2,y1),(255,0,255),t)
        cv2.line(img,(x2,y1),(x2,y1+l),(255,0,255),t)
        ## bottom right
        cv2.line(img,(x1,y2),(x1+l,y2),(255,0,255),t)
        cv2.line(img,(x1,y2-l),(x1,y2),color,t)
        ## bottom left
        cv2.line(img,(x2-l,y2),(x2,y2),color,t)
        cv2.line(img,(x2,y2-l),(x2,y2),color,t)
        return img
        



def main():
    cap=cv2.VideoCapture(1)
    # cap=cv2.VideoCapture('Images/Erica.mov')
    # cap=cv2.VideoCapture('Images/MiriamTap.mov')
    width =1280
    height= 720
    # width =640
    # height= 360
    
    # cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourrc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
    cap.set(cv2.CAP_PROP_FPS,30)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
    myFaceDetect=mpFaceDetect()
    while True:
        ret,img=cap.read()
        # cv2.flip(img,1)
        # img=cv2.resize(img,(0,0),fx=.5,fy=.5)
        img,bboxs=myFaceDetect.mpFaceProcess(img,draw=True,flip=True)
        # for i in bboxs:
        #     print(i[0],'  ',i[1][0][0],'  ',i[1][0][1],i[1][1][0],i[1][1][1])

        cTime=0
        pTime=0       
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        FPS=str(int(24*.80+fps*0.20))
        cv2.rectangle(img,(18,25),(200,75),(0,250,250),-1)
        cv2.putText(img,f'{FPS}fps',(25,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),2)
        # print(img.shape)
        cv2.imshow('Image',img)
        if cv2.waitKey(1)& 0xFF==27:
            break
    cap.release()
    cv2.destroyAllWindows()
if  __name__=='__main__':
    print('''INSTRUCTIONS:
          img,bboxs=myFaceDetect.mpFaceProcess(img,draw=True,flip=True)
          
          draw for drawing fancy border, flip=true to flip image for on mac webcam viewing''')
    
    main()