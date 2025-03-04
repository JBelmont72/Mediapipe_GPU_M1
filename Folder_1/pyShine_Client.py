'''

'''
# lets make the client code
import socket,cv2, pickle,struct

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host_ip = '192.168.1.20' # paste your server ip address here
PORT = 12345

host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
ADDR=(host_ip,PORT)## for some reason this worked better here
print('HOST IP:',host_ip)
socket_address = (host_ip,PORT) 


client_socket.connect(('192.168.1.30',PORT)) # a tuple
# client_socket.connect(('127.0.0.1',PORT)) # a tuple
data = b""
payload_size = struct.calcsize("Q")
while True:
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K
		if not packet: break
		data+=packet
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	while len(data) < msg_size:
		data += client_socket.recv(4*1024)
	frame_data = data[:msg_size]
	data  = data[msg_size:]
	frame = pickle.loads(frame_data)
	cv2.imshow("RECEIVING VIDEO",frame)
	key = cv2.waitKey(1) & 0xFF
	if key  == ord('q'):
		break
client_socket.close()