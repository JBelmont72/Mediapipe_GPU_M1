''''

'''

### WebSocket Server (Raspberry Pi Pico - MicroPython)

import uasyncio as asyncio
import network
import websocket
from machine import Pin

# Wi-Fi credentials
SSID = "your_SSID"
PASSWORD = "your_PASSWORD"

# Setup LED pin
led = Pin(15, Pin.OUT)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("Connected to Wi-Fi", wlan.ifconfig())

async def handle_client(websocket, path):
    global led
    async for message in websocket:
        finger_count = int(message)
        print(f"Received finger count: {finger_count}")
        
        if finger_count == 1:
            led.value(1)
            await websocket.send("LED ON")
        else:
            led.value(0)
            await websocket.send("LED OFF")

async def main():
    connect_wifi()
    server = await asyncio.start_server(
        lambda reader, writer: websocket.serve(handle_client, "0.0.0.0", 8765), "0.0.0.0", 8765
    )
    print("WebSocket server started on ws://0.0.0.0:8765")
    await server.wait_closed()

asyncio.run(main())
################################
# I'll provide WebSockets-based client and server implementations to enable bidirectional communication. The MacBook will send the finger count, and the Pico will send back a notification when the LED is turned on. Stay tuned while I prepare the code.

# Websockets Bidirectional
# Here's the WebSocket server implementation for the Raspberry Pi Pico. Now, I'll prepare the WebSocket client for your MacBook, which will send the finger count and receive LED status updates.

# I'll provide WebSockets-based client and server implementations to enable bidirectional communication. The MacBook will send the finger count, and the Pico will send back a notification when the LED is turned on. Stay tuned while I prepare the code.

# Websockets Bidirectional
# Here's the WebSocket server implementation for the Raspberry Pi Pico. Now, I'll prepare the WebSocket client for your MacBook, which will send the finger count and receive LED status updates.
# I'll provide WebSockets-based client and server implementations to enable bidirectional communication. The MacBook will send the finger count, and the Pico will send back a notification when the LED is turned on. Stay tuned while I prepare the code.

# Websockets Bidirectional
# Here's the WebSocket server implementation for the Raspberry Pi Pico. Now, I'll prepare the WebSocket client for your MacBook, which will send the finger count and receive LED status updates.
# ### WebSocket Server (Raspberry Pi Pico - MicroPython)

import uasyncio as asyncio
import network
import websocket
from machine import Pin

# Wi-Fi credentials
SSID = "your_SSID"
PASSWORD = "your_PASSWORD"

# Setup LED pin
led = Pin(15, Pin.OUT)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("Connected to Wi-Fi", wlan.ifconfig())

async def handle_client(websocket, path):
    global led
    async for message in websocket:
        finger_count = int(message)
        print(f"Received finger count: {finger_count}")
        
        if finger_count == 1:
            led.value(1)
            await websocket.send("LED ON")
        else:
            led.value(0)
            await websocket.send("LED OFF")

async def main():
    connect_wifi()
    server = await asyncio.start_server(
        lambda reader, writer: websocket.serve(handle_client, "0.0.0.0", 8765), "0.0.0.0", 8765
    )
    print("WebSocket server started on ws://0.0.0.0:8765")
    await server.wait_closed()

asyncio.run(main())

#########
### WebSocket Server (Raspberry Pi Pico - MicroPython)

import uasyncio as asyncio
import network
import websocket
from machine import Pin

# Wi-Fi credentials
SSID = "your_SSID"
PASSWORD = "your_PASSWORD"

# Setup LED pin
led = Pin(15, Pin.OUT)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("Connected to Wi-Fi", wlan.ifconfig())

async def handle_client(websocket, path):
    global led
    async for message in websocket:
        finger_count = int(message)
        print(f"Received finger count: {finger_count}")
        
        if finger_count == 1:
            led.value(1)
            await websocket.send("LED ON")
        else:
            led.value(0)
            await websocket.send("LED OFF")

async def main():
    connect_wifi()
    server = await asyncio.start_server(
        lambda reader, writer: websocket.serve(handle_client, "0.0.0.0", 8765), "0.0.0.0", 8765
    )
    print("WebSocket server started on ws://0.0.0.0:8765")
    await server.wait_closed()

asyncio.run(main())
########
# Here's the WebSocket client for your MacBook, which will send the finger count and receive LED status updates:

### WebSocket Client (MacBook - Python)

import asyncio
import websockets

async def send_finger_count():
    uri = "ws://your_pico_ip:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            finger_count = input("Enter finger count: ")  # Replace with your detection logic
            await websocket.send(finger_count)
            response = await websocket.recv()
            print(f"Received from Pico: {response}")

asyncio.run(send_finger_count())
# Replace "your_pico_ip" with the actual IP address of your Raspberry Pi Pico. This script continuously sends finger counts and prints the LED status updates received from the Pico. Let me know if you need further refinements!







# You said:
# can you send again the versions for WEBSOCKETS and enable bidirectional communication. I want to send back a notification from the pico that an led is turned on when the finger count is a specific value such as 1. Also, what are the advantages of WEBSOCKETS over socket and MQTT?
# ChatGPT said:
# ChatGPT
# Advantages of WebSockets Over Sockets and MQTT
# Real-Time, Full-Duplex Communication:
# Unlike traditional sockets, WebSockets allow simultaneous sending and receiving of messages without constant re-establishing of connections.
# MQTT, while efficient, follows a publish-subscribe model and introduces a slight delay due to the broker.
# Low Latency:
# WebSockets maintain an open connection, leading to faster communication than MQTT (which involves a broker) and traditional sockets (which require reconnections or polling).
# Lightweight and Efficient for Bidirectional Communication:
# WebSockets allow direct communication between the client and the server without the need for a third-party broker (as in MQTT).
# Traditional TCP/UDP sockets can be used similarly but require more manual handling of connection states.
# Better for Web-Based Applications:
# WebSockets are natively supported by web browsers


# Websockets Bidirectional



