'''

'''

import network
# import secrets
# import secrets_Condo
from time import sleep
class WiFi:
    def __init__(self):
        # self.ssid = secrets.ssid
        # self.ssid = 'NETGEAR48'
        #self.ssid = self.password
        #self.ssid = self.password
        self.ssid = 'SpectrumSetup-41'
        # self.password = secrets.password
        # self.password = 'waterypanda901'
        self.password = 'leastdinner914'
    
    def ConnectWiFi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        # wlan.connect(Secrets_Condo.ssid,Secrets_Condo.password)
        wlan.connect(self.ssid, self.password)
        sleep(1)
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
        ip = wlan.ifconfig()[0]
        print(f'Pico Connected on IP {ip}')
        return ip

    def AP_setup(self, ssid='PicoW_AP', password='12345678'):
        wlan = network.WLAN(network.AP_IF)  # Create AP interface
        wlan.config(essid=ssid, password=password,channel=6)  # Set SSID and password
        wlan.active(True)  # Activate AP mode
        # wlan.config(essid=ssid, password=password,channel=6)  # Set SSID and password
        sleep(2)
        print("AP Mode Enabled:", wlan.active())
        print("AP IP Address:", wlan.ifconfig())  # Default should be 192.168.4.1
        return wlan.ifconfig()[0]  # Return AP IP address
def main():
    myWifi=WiFi()
    while True:
        ip=myWifi.AP_setup()
        # ip=myWifi.ConnectWiFi()
        print(ip)
        # sleep(1)
       
# def main():
#     myWifi=WiFi()
#     while True:
#         ip=myWifi.AP_setup()
#         # ip=myWifi.ConnectWiFi()
#         print(ip)
#         sleep(1)
    
if __name__=='__main__':
    main()

#######~~~~~~~
