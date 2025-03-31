'''
This is the pure final socket version of the client side of the socket  to send fingercount to the pico server side with the serv0. 
This is also in FebChat along with options for changing to MQTT. copied to my Notes as well

The Pico Servo side is located in McWhorter WiFi Pico  in the fingerControl folder. The corresponding program for the server is: /Users/judsonbelmont/Documents/SharedFolders/Pico/MCWhorter_WiFi_Pico/HandControl/Finger_Servo_Control.py
A copy of that will also be at the bottom of this program:
Bottom is the socket server pico side with the servo
located in McWhoter WiFi Pico folder/repository. /Users/judsonbelmont/Documents/SharedFolders/Pico/MCWhorter_WiFi_Pico/HandControl/Finger_Servo_Control.py
if the pico server shows 'Pico Connected on IP 192.168.1.253'
Then need the client to : HOST = '192.168.1.253'
0.0.0.0 tells the server to listen on all available network interfaces, but the client cannot connect to 0.0.0.0.
Use the exact IP address assigned to the Pico by your Wi-Fi router.

I have two woring versions for the picoW servo finger counter Server
the First is the "Finger_Servo_Control.py and the second one is 'Servo_Socket.py'
Both are in McWhorter_WiFi_Pico repository
The handTrackModule and the finger counter programs are in Mediapipe_GPU_M1 repo and in the 'FingerControl' Folder
The working socket server program is at bottom.
In some development environments or with specific libraries (like MicroPython on the Pico), the connection to the Wi-Fi network may be implicitly established when the Pico starts
to set up a static IP:
wlan.ifconfig(('192.168.1.253', '255.255.255.0', '192.168.1.1', '8.8.8.8'))


'''
# 1. Fixing Your Function to Return Finger Count
# Your current function has a few issues:

# UnboundLocalError: totalFingers is not defined in some cases.
# Redundant imports inside the function.
# Looping indefinitely inside the function (while True). The function should process a single frame and return immediately.
# Here's a corrected version:



import cv2
import handTrackModule as ht
import time

import socket


# # Setup socket connection
# HOST = '0.0.0.0'  # Replace with Raspberry Pi Pico's IP
HOST = '192.168.1.253'


PORT = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Initialize the hand detector
detector= ht.mpHands(.75,.75)
tipIds = [4, 8, 12, 16, 20]  # Fingertip landmarks

# def count_fingers(img):
#     """Processes an image, detects the hand, and returns the number of fingers raised."""
#     img,myHands,handsType = detector.Marks(img)
#     # img = detector.findHands(img)
#     ##  lmList returns a list of lists, where each list corresponds to a hand. So, if there are multiple hands, you need to iterate over them.
#     lmList = detector.findPositions(img, draw=False)

#     if len(lmList) == 0:
#         return 0  # No hand detected

#     fingers = []
#     if len(lmList) != 0:
#         # Thumb (Different axis for detection)
#         if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:  # Adjust for left vs. right hand
#             fingers.append(1)
#         else:
#             fingers.append(0)

#         # Other fingers
#         for id in range(1, 5):
#             if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
#                 fingers.append(1)
#             else:
#                 fingers.append(0)

#         return fingers.count(1)  # Total fingers raised

###############~~~~~~~~ 24 March 25 version of above def countfingers()  to address lm out of range
# def count_fingers(img):
#     """Processes an image, detects the hand, and returns the number of fingers raised."""
#     img, myHands, handsType = detector.Marks(img)
#     all_lmLists = detector.findPositions(img, draw=False)  # List of hand landmarks

#     if len(all_lmLists) == 0:
#         print("No hands detected.")
#         return 0

#     for lmList in all_lmLists:
#         if len(lmList) < 21:
#             print(f"Incomplete landmark data. Found {len(lmList)} points.")
#             continue

#         print(f"Detected {len(lmList)} landmarks.")  # Debug
#         fingers = []
#         if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:  # Check thumb
#             fingers.append(1)
#         else:
#             fingers.append(0)

#         for id in range(1, 5):
#             if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
#                 fingers.append(1)
#             else:
#                 fingers.append(0)

#         return fingers.count(1)

#     return 0
#####~~~~~~~~~ 24 March 25 to modified to count fingers on both hands
# def count_fingers(img):
#     """Processes an image, detects the hands, and returns the number of fingers raised."""
#     img, myHands, handsType = detector.Marks(img)
#     all_lmLists = detector.findPositions(img, draw=False)

#     totalFingers = 0  # Sum of fingers from all hands

#     for lmList in all_lmLists:  # Loop through each hand
#         if len(lmList) == 0:
#             continue

#         fingers = []
#         for handType in handsType:
#             print(handType)
#             if handType == 'Right':
#                 # Thumb (check x-axis for thumb tip)
#                 if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:  # Check left or right thumb
#                     fingers.append(1)
#                 else:
#                     fingers.append(0)
#             if handType == 'Left':
#                 if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  # Check left or right thumb
#                     fingers.append(1)
#                 else:
#                     fingers.append(0)

#         # Other 4 fingers (check y-axis)
#         for id in range(1, 5):
#             if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
#                 fingers.append(1)
#             else:
#                 fingers.append(0)

#         # Add the count from this hand to the total
#         totalFingers += fingers.count(1)

#     return totalFingers

###~~~~~~~~~~
def count_fingers(img):
    """Processes an image, detects the hands, and returns the number of fingers raised."""
    img, myHands, handsType = detector.Marks(img)
    all_lmLists = detector.findPositions(img, draw=False)

    totalFingers = 0  # Sum of fingers from all hands
    for lmList, handType in zip(all_lmLists, handsType):  # Loop through each hand with handType
        if len(lmList) < 21:  # Ensure all landmarks are detected
            continue

        fingers = []  # Reset for each hand

        # Thumb logic
        if handType == 'Left':
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  # Check left or right thumb
            # if lmList[4][1] > lmList[3][1]:  # For right hand, thumb open if tip is to the right
                fingers.append(1)
            else:
                fingers.append(0)
        elif handType == 'Right':
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:  # Check left or right thumb
            # if lmList[4][1] < lmList[3][1]:  # For left hand, thumb open if tip is to the left
                fingers.append(1)
            else:
                fingers.append(0)

        # Check other fingers (same logic for both hands)
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:  # Check y-axis
                fingers.append(1)
            else:
                fingers.append(0)

        # Add the count from this hand to the total
        totalFingers += fingers.count(1)

    # for lmList in all_lmLists:  # Loop through each hand
    #     if len(lmList) == 0:
    #         continue

    #     fingers = []
    #     for handType in handsType:
    #         print(handType)
    #         if handType == 'Right':
    #             # Thumb (check x-axis for thumb tip)
    #             if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:  # Check left or right thumb
    #                 fingers.append(1)
    #             else:
    #                 fingers.append(0)
    #         if handType == 'Left':
    #             if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  # Check left or right thumb
    #                 fingers.append(1)
    #             else:
    #                 fingers.append(0)

    #     # Other 4 fingers (check y-axis)
    #     for id in range(1, 5):
    #         if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
    #             fingers.append(1)
    #         else:
    #             fingers.append(0)

    #     # Add the count from this hand to the total
    #     totalFingers += fingers.count(1)

    return totalFingers

################# 2. Capturing Video and Using the Function
wCam, hCam = 1280, 760
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
pTime=0
folderPath = "/Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/Images/FingerCount"

myList=['a6.png','a1.png', 'a2.png', 'a3.png', 'a4.png', 'a5.png','a7.png','a8.png','a9.png','a10.png','a6.png']
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    image=cv2.resize(image,(360,480))
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))
# print(overlayList[0])
# print("image  ",image.shape)
pTime = 0

while True:
    success, img = cap.read()
    if not success:
        break
    ####~~~~~~~~
    # Limit totalFingers to the maximum index of overlayList Use this if less .png than fingers
    # totalFingers = min(totalFingers, len(overlayList) - 1)

    # Now it's safe to access overlayList
    # h, w, c = overlayList[totalFingers].shape
    ####~~~~~~~~~~~~~~
    totalFingers = count_fingers(img)   ## number of fingers returned
    totalFingers = min(totalFingers, len(overlayList) - 1)
    print(f'Finger Count: {totalFingers}')
    
    print(f'Sending: {totalFingers}')   
    ### Send finger count as a string
    
    ### client_socket.sendall(str(totalFingers).encode()) NEED to add a new line break
    client_socket.sendall(f"{totalFingers}\n".encode())

    h,w,c =overlayList[totalFingers].shape  ## gets the shape of the specific .png whose index corresponds to the # of fingers 
        # print(h,w,c)
    img[0:int(h),0:int(w)]=overlayList[totalFingers]
    cv2.rectangle(img, (20, hCam-40), (170, hCam-200), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(totalFingers), (45, hCam-80), cv2.FONT_HERSHEY_PLAIN,
                10, (255, 0, 0), 25)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break
client_socket.close()
cap.release()
cv2.destroyAllWindows()

#####~~~~~~below is the socket server pico side with the servo
## located in McWhoter WiFi Pico folder/repository. /Users/judsonbelmont/Documents/SharedFolders/Pico/MCWhorter_WiFi_Pico/HandControl/Finger_Servo_Control.py

# import socket
# import machine
# from time import sleep
## I was able to run this on my computer without this because I am already with a wifi connection.And only needed the
# import network

# ssid = "SpectrumSetup-41"
# password = "leastdinner914"

# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect(ssid, password)

# # Wait until connected
# while not wlan.isconnected():
#     pass

# print("Connected to Wi-Fi")
# ip = wlan.ifconfig()[0]
# print(f"Pico Connected on IP {ip}")





# # Pin setup for the servo
# servo_pin = machine.PWM(machine.Pin(0))  # Use Pin 15 for servo
# servo_pin.freq(50)

# # Define servo angle limits and pulse width range
# MIN_ANGLE = 0
# MAX_ANGLE = 180
# MIN_DUTY = 1000
# MAX_DUTY = 9000

# # Set delay between updates (in seconds)
# UPDATE_DELAY = 0.1  # Delay of 100ms between updates

# # Function to set servo angle
# def set_servo_angle(angle):
#     duty = int(MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY))
#     servo_pin.duty_u16(duty)
#     print(f"Servo angle set to {angle} degrees (duty cycle: {duty})")

# # Create a socket server
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('0.0.0.0', 12345))
# server_socket.listen(1)

# print("Pico Connected on IP 192.168.1.253")
# print("Listening on ('0.0.0.0', 12345)")

# # Main server loop
# try:
#     while True:
#         print("Waiting for connection...")
#         conn, addr = server_socket.accept()
#         print(f"Connected by {addr}")
        
#         last_angle = -1  # Track the last angle to prevent unnecessary updates
        
#         buffer = ""  # Buffer to hold incomplete data

#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break

#             # Decode and add received data to the buffer
#             buffer += data.decode()

#             # Split buffer by newlines and process each part
#             parts = buffer.split('\n')

#             # Process all parts except the last (which may be incomplete)
#             for part in parts[:-1]:
#                 part = part.strip()
#                 if part.isdigit():
#                     finger_count = int(part)
#                     angle = int((finger_count / 10) * 180)

#                     # Update servo only if the angle changes
#                     if angle != last_angle:
#                         set_servo_angle(angle)
#                         last_angle = angle
#                         sleep(UPDATE_DELAY)
#                 else:
#                     print(f"Non-numeric data received: '{part}'. Skipping...")

#             # Keep the incomplete part in the buffer
#             buffer = parts[-1]

#         conn.close()
#         print("Connection closed. Waiting for next connection...")

# except KeyboardInterrupt:
#     print("Server shutting down...")
#     server_socket.close()