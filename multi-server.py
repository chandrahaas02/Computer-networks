from _thread import *
import threading
import socket
import time
import sys
from datetime import datetime

MAX_CLIENTS = 10
client_list=[]
client_names=[]

my_lock = threading.Lock() 

def threaded(conn,name):
    while True:
        message = conn.recv(1024)
        if not message:
            print(name+" connection closed")
            break
        command=message.decode().split(" ")
        if command[0]=="get_list":
            friends = client_names.copy()
            friends.remove(name)
            msg="friends in the room : "+" ".join(friends)
            msg=msg.encode()
            conn.send(msg)
        
        elif command[0]=="send" and command[1]=="all" and len(command)>=3:
            for (names,connec) in client_list:
                if connec != conn:
                    msg=name+" :"+" ".join(command[2:])
                    connec.send(msg.encode())
        
        elif command[0]=="send":
            div=command.index(":")
            list_of_c=command[1:div]
            msg=name+" :"+" ".join(command[div+1:])
            for (names,connec) in client_list:
                if names in list_of_c:
                    connec.send(msg.encode())
                    list_of_c.remove(names)
        elif command[0]=="file":
            div=command.index(":")
            list_of_c=command[1:div]
            msg="file"+" ".join(command[div+1:])
            for (names,connec) in client_list:
                if names in list_of_c:
                    connec.send(msg.encode())
                    list_of_c.remove(names)
    conn.close()
    client_list.remove((name,conn))

if __name__ == '__main__':

    s_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating socket
    s_hostname = socket.gethostname() # retrieving hostname
    s_ip = socket.gethostbyname(s_hostname) # get ip of host
    port = 9992
    s_soc.bind((s_ip,port)) #binding host to port
    print("IP of server :",s_ip)
    name = input('Enter name of Server:')
    s_soc.listen(MAX_CLIENTS)
    print("In Listen mode....")


    while True:
        conn, add = s_soc.accept() # accepting connection  
        c_message = conn.recv(1024)
        name_of_client=c_message.decode()
        msg="Welcome your friend "+ name_of_client+ " to the party"
        msg=msg.encode()
        for (name,conect) in client_list :
            conect.send(msg)
        print("Name of client: ",name_of_client)
        client_list.append((name_of_client,conn))
        client_names.append(name_of_client)
        conn.send(name.encode())
        start_new_thread(threaded, (conn,name_of_client))
    s_soc.close()


