from asyncio import sleep
import os
import socket
import threading
import time

def filelist(path):
    filelist = ""
    files = os.listdir(path)
    for file in files:
        filelist += file + ","
    return filelist.rstrip(filelist[-1])

def listener():
    while True:
        data = client_socket.recv(1024).decode()
        print(data)
        if data == "Event: signed out":
            quit()
            

host = socket.gethostname()
port = 5000


client_socket = socket.socket()
client_socket.connect((host, port))

threading.Thread(target=listener).start()

message = input("\x1b[6;30;42mEpiloges:\x1b[0m \n Signin\n-> ")
while not message.startswith('Signin'):
    message = input("\x1b[6;30;42mEpiloges:\x1b[0m \n Signin\n-> ")

list = filelist('D:/Documents/GitHub/python-socket/tcp')
message=message+","+list
client_socket.send(message.encode())
print ("\x1b[6;30;42mEpiloges:\x1b[0m \n Signout\n Search <keywords>\n")
while True:
    message = input("")
    client_socket.send(message.encode())
    time.sleep(1)