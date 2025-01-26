
import sys
import cv2
import time
import tensorflow as tf
print(cv2.__version__)
import numpy as np
print(f"This is version {sys.version}")
print(np.__version__)
cam=cv2.VideoCapture(1)
width=1280
height=720
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
print(cam.get(3),' x ',cam.get(4))
thickness = 5
fontH = 2
fontThickness = 4
filt=30
lastTime=time.time()
print(lastTime)
tickTime=time.thread_time()
print(tickTime)
time.sleep(.2)


# imageBGR = np.zeros([512,512,3],np.uint8)
# image = cv2.imread('/Users/judsonbelmont/Documents/Projects/OpenCV_2/images/lena.jpg',1)
while True:     #if true then the first arguement (ret) is true and the frame is captured
    ret,image=cam.read()
    frameTime=time.time()-lastTime
    lastTime=time.time()
    print(frameTime)
    fps=1/frameTime
    print('fps',round(fps,2))
    filt=filt*.97+fps*.03
    filt=round(filt,1)
        
    
    # imageBGR[:,:]=(255,0,0)
    # imageBGR =cv2.cvtColor(imageBGR,cv2.COLOR_BGR2RGB)
    image1 = cv2.line(image,(0,0),(int(.5*width),int(0.25*height)),(255,0,0),thickness,4)
    image2 = cv2.line(image,(300,255),(500,0),(182,100,202),thickness,4)
    image3 = cv2.arrowedLine(image,(0,300),(200,300),(125,125,0),thickness,6)
    image4 =cv2.rectangle(image,(20,20),(170,60),(0,75,125),-1)
    imageFPS=cv2.putText(image,str(filt)+' FPS',(20,55),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
    image5 =cv2.rectangle(image,(400,0),(510,500),(0,0,255),7)
    image6 =cv2.circle(image,(250,250),25,(125,125,0),4)
    image7 =cv2.putText(image,'This is fun!',(20,400),cv2.FONT_HERSHEY_TRIPLEX,fontH,(255,255,255),fontThickness,cv2.LINE_4)
    cv2.imshow('image',image)
    # cv2.imshow('BGR Image',imageBGR)
    if cv2.waitKey(1) & 0xff ==ord('c'):
        break
cam.release()
cv2.destroyAllWindows()
 