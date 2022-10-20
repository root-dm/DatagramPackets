import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 5050))
print ("Server started")
registered=[]

def new_client(message, caddr):
    print("Connection from: " + str(caddr[0]+":"+str(caddr[1])))
    data = message
    if str(data).startswith('Signin'):
        name = str(data).replace('Signin ', '')
        user={"name": name, "ip": caddr}
        registered.append(user)
        data="\n\033[92m(!)\033[0m Registered, welcome \033[92m"+name+"\033[0m"
        print (str(caddr)+" / " + name +" - registered!")
        server_socket.sendto(data.encode(), caddr)

        callback_message="\n\033[92m(!)\033[0m \033[92m"+name+"\033[0m has signed in"
        for user in registered:
            if user["ip"] != caddr:
                server_socket.sendto(callback_message.encode(), user["ip"])
    elif str(data).startswith('Signout'):
        for user in registered:
            if user["ip"]==caddr:
                registered.remove(user)
                data="\n\033[92m(!)\033[0m Signed out, goodbye \033[92m"+user["name"]+"\033[0m"
                server_socket.sendto(data.encode(), user["ip"])

                callback_message="\n\033[92m(!)\033[0m \033[92m"+user["name"]+"\033[0m has signed out"
                for user in registered:
                    if user["ip"] != caddr:
                        server_socket.sendto(callback_message.encode(), user["ip"])
    elif str(data).startswith('Message'):
        message = str(data).replace('Message ', '')
        callback_message=""
        cnt_received=0
        delivered=False
        for user in registered:
            if user["ip"] == caddr:
                callback_message="\033[1m"+user["name"]+":\033[0m "+message

        for user in registered:
            # if user["ip"] != caddr:
            server_socket.sendto(callback_message.encode(), user["ip"])
            cnt_received+=1
            delivered=True
        if cnt_received==0:
            msg="\n\033[91m(!)\033[0m No users online\n"
            server_socket.sendto(msg.encode(), caddr)
        if delivered==False:
            msg="\n\033[91m(!)\033[0m Message not delivered\n"
            server_socket.sendto(msg.encode(), caddr)

while True:
    message, address = server_socket.recvfrom(1024)
    new_client(message.decode(), address)
    