from asyncio import sleep
import socket
import threading
import time

def listener():
    while True:
        try:
            data = UDPClientSocket.recv(1024).decode()
            print (data)
        except:
            data=""

serverAddressPort   = ("127.0.0.1", 5050)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
threading.Thread(target=listener).start()

message = input("\x1b[6;30;42mEpiloges:\x1b[0m \n Signin <username>\n-> ")
while not message.startswith('Signin'):
    message = input("\x1b[6;30;42mEpiloges:\x1b[0m \n Signin <username>\n-> ")

UDPClientSocket.sendto(message.encode(), serverAddressPort)
print ("\x1b[6;30;42mEpiloges:\x1b[0m \n Signout\n Message <message>\n")
while True:
    message = input("")
    UDPClientSocket.sendto(message.encode(), serverAddressPort)
    time.sleep(1)