import cv2
import numpy as np

class FacialRecognitionSystem:
    def __init__(self, camera_index=1):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        self.face_cascade = cv2.CascadeClassifier('/Users/judsonbelmont/Documents/Shared_Folders/OpenCV_3/haar/haarcascade_frontalcatface.xml')
        self.smile_cascade = cv2.CascadeClassifier('/Users/judsonbelmont/Documents/Shared_Folders/OpenCV_3/haar/haarcascade_smile.xml')
        self.face_rect = None
        self.smile_rect = None
        self.is_smiling = False
        self.running = True

    def run(self):
       while self.running:
           ret, frame = self.cap.read()
           if not ret:
               print("Failed to grab frame")
               break

           gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
           faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
           smiles = self.smile_cascade.detectMultiScale(gray, 1.5, 4)

           for (x, y, w, h) in faces:
               self.face_rect = (x, y, w, h)
               cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

               # Detect smile in the face region
               roi_gray = gray[y:y+h, x:x+w]
               smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.5, 4)
               if smiles:
                   self.is_smiling = True
                   cv2.rectangle(frame, (x + int(w/2) - 10, y + int(h/2) - 10), (0, 255, 0), 2)
                   break  # Stop searching for faces after finding a smile
               else:
                   self.is_smiling = False

           cv2.imshow('Facial Recognition', frame)

           if cv2.waitKey(1) & 0xFF == ord('q'):
               self.running = False

       self.cap.release()
       cv2.destroyAllWindows()


if __name__ == '__main__':
   system = FacialRecognitionSystem()
   system.run()