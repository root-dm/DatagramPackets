from asyncio import sleep
import socket
import threading
import time

def listener():
    while True:
        data = client_socket.recv(1024).decode()
        print(data)
        if data == "Event: signed out":
            quit()
            

host = socket.gethostname()
print (host)
port = 5000


client_socket = socket.socket()
client_socket.connect((host, port))

threading.Thread(target=listener).start()

message = input("\x1b[6;30;42mEpiloges:\x1b[0m \n Signin <username>\n-> ")
while not message.startswith('Signin'):
    message = input("\x1b[6;30;42mEpiloges:\x1b[0m \n Signin <username>\n-> ")

client_socket.send(message.encode())
print ("\x1b[6;30;42mEpiloges:\x1b[0m \n Signout\n Message <message>\n")
while True:
    message = input("")
    client_socket.send(message.encode())
    time.sleep(1)