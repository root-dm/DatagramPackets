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
            name = str(data).replace('Signin ', '')
            ip = str(str(caddr[0])+":"+str(caddr[1]))
            user={"name": name, "ip": ip, "socket": csocket}
            registered.append(user)
            data="\n\033[92m(!)\033[0m Registered, welcome \033[92m"+name+"\033[0m"
            print (ip+" / " + name +" - registered!")
            csocket.send(data.encode())

            callback_message="\n\033[92m(!)\033[0m \033[92m"+name+"\033[0m has signed in"
            for user in registered:
                if user["ip"] != str(str(caddr[0])+":"+str(caddr[1])):
                    user["socket"].send(callback_message.encode())
        elif str(data).startswith('Signout'):
            for user in registered:
                if user["ip"]==str(str(caddr[0])+":"+str(caddr[1])):
                    registered.remove(user)
                    data="\n\033[92m(!)\033[0m Signed out, goodbye \033[92m"+user["name"]+"\033[0m"
                    csocket.send(data.encode())
                    csocket.send("Event: signed out".encode())
                    csocket.close()

                    callback_message="\n\033[92m(!)\033[0m \033[92m"+user["name"]+"\033[0m has signed out"
                    for user in registered:
                        if user["ip"] != str(str(caddr[0])+":"+str(caddr[1])):
                            user["socket"].send(callback_message.encode())
        #elif str(data).startswith('Message'):
        else:
            # print ("Message handler\n----") #DEBUG
            # message = str(data).replace('Message ', '')
            message = str(data)
            callback_message=NULL
            cnt_received=0
            delivered=False
            for user in registered:
                if user["ip"] == str(str(caddr[0])+":"+str(caddr[1])):
                    callback_message="\033[1m"+user["name"]+":\033[0m "+message

            for user in registered:
                if user["ip"] != str(str(caddr[0])+":"+str(caddr[1])):
                    user["socket"].send(callback_message.encode())
                    cnt_received+=1
                    delivered=True
            if cnt_received==0:
                msg="\n\033[91m(!)\033[0m No users online\n"
                csocket.send(msg.encode())
            if delivered==False:
                msg="\n\033[91m(!)\033[0m Message not delivered\n"
                csocket.send(msg.encode())
        # else:
        #     csocket.send("Invalid command".encode())


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