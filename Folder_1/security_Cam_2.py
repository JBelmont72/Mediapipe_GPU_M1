'''

'''
import sys
import cv2
import time
import datetime
import socket, pickle,struct,imutils
print(cv2.__version__)
import numpy as np
print(f"This is version {sys.version}")
print(np.__version__)
cam=cv2.VideoCapture(1)
width=1280
height=720


# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host_name  = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
# host_ip = "75.68.100.114"
host_ip='127.0.0.1'
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)
# Socket Bind
server_socket.bind(socket_address)
# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)


cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 20)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'mp4v'))


face_cascade = cv2.CascadeClassifier(
    'haarCascades/haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier(
    # cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
     "haarCascades/haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(cam.get(3)), int(cam.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

while True:
    _, frame = cam.read()
    client_socket,addr = server_socket.accept()
    print('GOT CONNECTION FROM:',addr)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)
    while cam.isOpened():
        a = pickle.dumps(frame)
        frame = imutils.resize(frame,width=320)
        message = struct.pack("Q",len(a))+a
        client_socket.sendall(message)
        if len(faces) + len(bodies) > 0:
            if detection:
                timer_started = False
            else:
                detection = True
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                out = cv2.VideoWriter(
                    f"{current_time}.mp4", fourcc, 20, frame_size)
                print("Started Recording!")
        elif detection:
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    detection = False
                    timer_started = False
                    out.release()
                    print('Stop Recording!')
            else:
                timer_started = True
                detection_stopped_time = time.time()

        if detection:
            out.write(frame)

        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    # a = pickle.dumps(frame)
    # frame = imutils.resize(frame,width=320)
    # message = struct.pack("Q",len(a))+a
    # client_socket.sendall(message)
            
        cv2.imshow('TRANSMITTING VIDEO',frame)
        key = cv2.waitKey(1) & 0xFF
        if key ==ord('q'):
            client_socket.close()
            break
    # cv2.imshow("Camera", frame)

    # if cv2.waitKey(1) == ord('q'):
    #     break

    out.release()
    cam.release()
    cv2.destroyAllWindows()
######~~~~~~~~
# import socket, cv2, pickle,struct,imutils

# # Socket Create
# server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# # host_name  = socket.gethostname()
# # host_ip = socket.gethostbyname(host_name)
# # host_ip = "75.68.100.114"
# host_ip='192.168.1.12'
# print('HOST IP:',host_ip)
# port = 9999
# socket_address = (host_ip,port)

# # Socket Bind
# server_socket.bind(socket_address)

# # Socket Listen
# server_socket.listen(5)
# print("LISTENING AT:",socket_address)

# Socket Accept
# while True:
# 	client_socket,addr = server_socket.accept()
# 	print('GOT CONNECTION FROM:',addr)
# 	if client_socket:
# 		vid = cv2.VideoCapture(0)
		
# 		while(vid.isOpened()):
# 			img,frame = vid.read()
# 			frame = imutils.resize(frame,width=320)
# 			a = pickle.dumps(frame)
# 			message = struct.pack("Q",len(a))+a
# 			client_socket.sendall(message)
			
# 			cv2.imshow('TRANSMITTING VIDEO',frame)
# 			key = cv2.waitKey(1) & 0xFF
# 			if key ==ord('q'):
# 				client_socket.close()