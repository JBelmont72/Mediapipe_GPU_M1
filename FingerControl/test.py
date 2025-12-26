import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera failed to initialize")
else:
    print("Camera connected successfully")
    cap.release()
