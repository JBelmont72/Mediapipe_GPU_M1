
# 1. Fixing Your Function to Return Finger Count
# Your current function has a few issues:

# UnboundLocalError: totalFingers is not defined in some cases.
# Redundant imports inside the function.
# Looping indefinitely inside the function (while True). The function should process a single frame and return immediately.
# Here's a corrected version:



import cv2
import handTrackModule as ht
import time

# import socket


# # Setup socket connection
# HOST = '192.168.1.100'  # Replace with Raspberry Pi Pico's IP
# PORT = 65432
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))



# Initialize the hand detector
detector = ht.handDetector(.75, .75)
tipIds = [4, 8, 12, 16, 20]  # Fingertip landmarks

def count_fingers(img):
    """Processes an image, detects the hand, and returns the number of fingers raised."""
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) == 0:
        return 0  # No hand detected

    fingers = []

    # Thumb (Different axis for detection)
    if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:  # Adjust for left vs. right hand
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for id in range(1, 5):
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)  # Total fingers raised


################# 2. Capturing Video and Using the Function
wCam, hCam = 1280, 760
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
pTime=0
folderPath = "/Users/judsonbelmont/Documents/SharedFolders/Mediapipe/Mediapipe_GPU_M1/Images/FingerCount"


myList=['a6.png','a1.png', 'a2.png', 'a3.png', 'a4.png', 'a5.png']
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
    
    totalFingers = count_fingers(img)   ## number of fingers returned
    print(f'Finger Count: {totalFingers}')
    
    #     print(f'Sending: {totalFingers}')   
    # Send finger count as a string
    #     client_socket.sendall(str(totalFingers).encode())
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
# client_socket.close()
cap.release()
cv2.destroyAllWindows()
################
 

# 3. Sending Finger Count to Raspberry Pi Pico
# We will use Python's socket library to send the finger count over a local network.

# Client (MacBook) - Sends Finger Count

# import socket
# import cv2

# # Setup socket connection
# HOST = '192.168.1.100'  # Replace with Raspberry Pi Pico's IP
# PORT = 65432
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))

# # Start video capture
# cap = cv2.VideoCapture(1)
# cap.set(3, 1280)
# cap.set(4, 760)

# while True:
#     success, img = cap.read()
#     if not success:
#         break

#     totalFingers = count_fingers(img)
#     print(f'Sending: {totalFingers}')
    
#     # Send finger count as a string
#     client_socket.sendall(str(totalFingers).encode())

#     cv2.imshow("Image", img)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# client_socket.close()
# cap.release()
# cv2.destroyAllWindows()

######4. Receiving Data on Raspberry Pi Pico
# Server (Raspberry Pi Pico) - Controls Servo
'''
import socket
import machine
import time

# Initialize servo on GPIO 15
servo = machine.PWM(machine.Pin(15))
servo.freq(50)

def set_servo_angle(angle):
    """Converts an angle (0-180) to a duty cycle for the servo."""
    duty = int((angle / 180) * 1023)  # Convert 0-180 degrees to duty cycle
    servo.duty_u16(duty)

# Setup server
HOST = '0.0.0.0'
PORT = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break

    finger_count = int(data.decode().strip())
    print(f"Received: {finger_count}")

    # Map finger count to servo angles
    angle = finger_count * 30  # Example: 0 fingers → 0°, 5 fingers → 150°
    set_servo_angle(angle)
    time.sleep(0.5)

conn.close()
server_socket.close()

#############5. Required Libraries
# MacBook (Client)
# cv2 (OpenCV)
# handTrackModule (Your custom module)
# socket (Built-in)
# Raspberry Pi Pico (Server)
# machine (MicroPython for GPIO control)
# socket (MicroPython for networking)
# time
# 6. Alternative to Sockets?
# A better option than a socket would be:

# MQTT (Message Queuing Telemetry Transport) – Efficient for IoT.
# WebSockets – For real-time, bidirectional communication.
# If you want a lightweight solution, sockets are fine for now. If you later scale your project (multiple devices, cloud integration), MQTT would be better.

# Would you like an MQTT version? 🚀


############MQTT VERSION alternative
# We'll use MQTT (Message Queuing Telemetry Transport) to communicate between your MacBook (which detects the finger count) and the Raspberry Pi Pico (which controls the servo motor).

# Plan:
# MacBook (Publisher)
# Detects fingers using OpenCV and MediaPipe.
# Publishes the finger count to an MQTT broker.
# Raspberry Pi Pico (Subscriber)
# Listens for messages from the MacBook.
# Moves a servo motor based on the received finger count.
# Step 1: Install MQTT Broker

# You'll need an MQTT broker to facilitate communication. You can either:

# Use a cloud-based broker like Eclipse Mosquitto.
# Run a local Mosquitto broker on your MacBook (brew install mosquitto).
# Step 2: Install MQTT Libraries

# On the MacBook:

pip install paho-mqtt

# on the pico MicroPython
import mip
mip.install("umqtt.simple")
# Step 3: MacBook (MQTT Publisher)

# Modify your finger-detection program to publish the finger count to an MQTT topic.

import cv2
import time
import paho.mqtt.client as mqtt
import handTrackModule as ht

BROKER = "your.mqtt.broker.ip"  # Replace with your broker IP
TOPIC = "pico/finger_count"

# Initialize MQTT Client
client = mqtt.Client()
client.connect(BROKER, 1883, 60)

We'll use MQTT (Message Queuing Telemetry Transport) to communicate between your MacBook and the Raspberry Pi Pico.

Steps to Implement:
Set up an MQTT broker
Use a public broker (e.g., test.mosquitto.org) or install Mosquitto on your Mac (brew install mosquitto).
Start the broker: mosquitto -v.
MacBook (Publisher - Sends Finger Count)
Use paho-mqtt to send the detected finger count.
Install the library:
bash
Copy
Edit
pip install paho-mqtt
Publish the finger count to a topic (e.g., "finger/count").
Raspberry Pi Pico (Subscriber - Controls Servo)
Use umqtt.simple to subscribe to "finger/count".
When a new count is received, move the servo accordingly.
Would you like example code for both sides?







4o
You said:
yes
ChatGPT said:
ChatGPT
1️⃣ MacBook (Publisher) - Sends Finger Count via MQTT
This script detects the number of raised fingers and publishes the count to an MQTT topic.

python
Copy
Edit
import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt

# MQTT Configuration
BROKER = "test.mosquitto.org"  # Use a local broker if preferred
TOPIC = "finger/count"
client = mqtt.Client()
client.connect(BROKER, 1883, 60)

# Mediapipe Setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def count_fingers(lm_list):
    fingers = [lm_list[i][2] < lm_list[i - 2][2] for i in [8, 12, 16, 20]]
    return sum(fingers) + (lm_list[4][1] > lm_list[3][1])  # Thumb condition

# OpenCV Loop
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = [(i, int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for i, lm in enumerate(hand_landmarks.landmark)]
            finger_count = count_fingers(lm_list)
            client.publish(TOPIC, str(finger_count))
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Finger Count", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
client.disconnect()
2️⃣ Raspberry Pi Pico (Subscriber) - Controls Servo
This script subscribes to the MQTT topic and moves a servo based on the received finger count.

python
Copy
Edit
import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, PWM

# Wi-Fi Configuration
SSID = "your_wifi_ssid"
PASSWORD = "your_wifi_password"

# MQTT Configuration
BROKER = "test.mosquitto.org"
TOPIC = "finger/count"

# Servo Setup
servo = PWM(Pin(15))
servo.freq(50)

def set_angle(angle):
    duty = int((angle / 180) * 5000 + 1000)  # Convert angle to duty cycle
    servo.duty_u16(duty)

def on_message(topic, msg):
    try:
        count = int(msg.decode())
        angle = count * 30  # Map count (0-5) to angle (0-150)
        set_angle(angle)
    except ValueError:
        pass

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(1)

# Connect to MQTT Broker
client = MQTTClient("pico", BROKER)
client.set_callback(on_message)
client.connect()
client.subscribe(TOPIC)

# Listen for MQTT messages
while True:
    client.check_msg()
    time.sleep(0.1)
🔗 How It Works
The MacBook detects fingers, counts them, and sends the count via MQTT.
The Pico listens for messages and moves the servo accordingly.
'''
