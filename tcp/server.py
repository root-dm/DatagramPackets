from asyncio.windows_events import NULL
from atexit import register
import socket
import array
import threading

def new_client(csocket, caddr):
    print("Connection from: " + str(caddr[0]+":"+str(caddr[1])))
    while True:
        data = csocket.recv(1024).decode()
        if not data:
            break
        if str(data).startswith('Signin'):
            filelist = str(data).replace('Signin,', '')
            filelist = filelist.split(',')
            ip = str(str(caddr[0])+":"+str(caddr[1]))
            user={"ip": ip, "files": filelist, "socket": csocket}
            registered.append(user)
        elif str(data).startswith('Signout'):
            for user in registered:
                if user["ip"]==str(str(caddr[0])+":"+str(caddr[1])):
                    registered.remove(user)
        elif str(data).startswith('Search'):
            message = str(data).replace('Search ', '')
            keywords = message.split()
            callback_message="Results\n"
            for user in registered:
                print (user["files"])
                for file in user["files"]:
                    for keyword in keywords:
                        if keyword in file:
                            callback_message+=file+":"+user['ip']+"\n"

            csocket.send(callback_message.encode())


server_socket = socket.socket()
host = socket.gethostname()
port = 5000

print ("Service started")
print ("Listening...")
server_socket.bind((host, port))
registered=[]
server_socket.listen(50)
while True:
    conn, address = server_socket.accept()
    threading.Thread(target=new_client, args=(conn, address)).start()