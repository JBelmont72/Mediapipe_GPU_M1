'''

'''

# import network
# # import secrets
# # import secrets_Condo
# from time import sleep
# class WiFi:
#     def __init__(self):
#         # self.ssid = secrets.ssid
#         self.ssid = 'NETGEAR48'
#         #self.ssid = self.password
#         #self.ssid = self.password
#         # self.ssid = 'SpectrumSetup-41'
#         # self.password = secrets.password
#         self.password = 'waterypanda901'
#         # self.password = 'leastdinner914'
    
#     def ConnectWiFi(self):
#         wlan = network.WLAN(network.STA_IF)
#         wlan.active(True)
#         #wlan.connect(Secrets_Condo.ssid,Secrets_Condo.password)
#         wlan.connect(self.ssid, self.password)
#         sleep(1)
#         while wlan.isconnected() == False:
#             print('Waiting for connection...')
#             sleep(1)
#         ip = wlan.ifconfig()[0]
#         print(f'Pico Connected on IP {ip}')
#         return ip

#     def AP_setup(self, ssid='PicoW_AP', password='12345678'):
#         wlan = network.WLAN(network.AP_IF)  # Create AP interface
#         wlan.config(essid=ssid, password=password,channel=6)  # Set SSID and password
#         wlan.active(True)  # Activate AP mode
#         # wlan.config(essid=ssid, password=password,channel=6)  # Set SSID and password
#         sleep(2)
#         print("AP Mode Enabled:", wlan.active())
#         print("AP IP Address:", wlan.ifconfig())  # Default should be 192.168.4.1
#         return wlan.ifconfig()[0]  # Return AP IP address
# def main():
#     myWifi=WiFi()
#     while True:
#         ip=myWifi.AP_setup()
#         # ip=myWifi.ConnectWiFi()
#         print(ip)
#         # sleep(1)
       
# # def main():
# #     myWifi=WiFi()
# #     while True:
# #         ip=myWifi.AP_setup()
# #         # ip=myWifi.ConnectWiFi()
# #         print(ip)
# #         sleep(1)
    
# if __name__=='__main__':
#     main()

#######~~~~~~~
# import module
import os
SSID = 'NETGEAR48"'
# function to establish a new connection
def createNewConnection(name, SSID, password):
	config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
	<name>"""+name+"""</name>
	<SSIDConfig>
		<SSID>
			<name>"""+SSID+"""</name>
		</SSID>
	</SSIDConfig>
	<connectionType>ESS</connectionType>
	<connectionMode>auto</connectionMode>
	<MSM>
		<security>
			<authEncryption>
				<authentication>WPA2PSK</authentication>
				<encryption>AES</encryption>
				<useOneX>false</useOneX>
			</authEncryption>
			<sharedKey>
				<keyType>passPhrase</keyType>
				<protected>false</protected>
				<keyMaterial>"""+password+"""</keyMaterial>
			</sharedKey>
		</security>
	</MSM>
</WLANProfile>"""
	command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
	with open(name+".xml", 'w') as file:
		file.write(config)
	os.system(command)

# function to connect to a network 
def connect(name, SSID):
	command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
	os.system(command)

# function to display avavilabe Wifi networks 
def displayAvailableNetworks():
	command = "netsh wlan show networks interface=Wi-Fi"
	os.system(command)


# display available netwroks
displayAvailableNetworks()

# input wifi name and password
name = input("Name of Wi-Fi: ")
password = input("Password: ")

# establish new connection
createNewConnection(name, name, password)

# connect to the wifi network
connect(name, name)
print("If you aren't connected to this network, try connecting with the correct password!")
