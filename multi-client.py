from _thread import *
import threading
import socket
import time
import sys
from datetime import datetime
import os 


def writing():
    while True:
        msg=c_socket.recv(1024)
        msg=msg.decode()
        if msg[:4]=="file":
            div=msg.index(",")
            filename =msg[4:div]
            # print(filename)
            f = open(filename,"w")
            f.write(msg[div+1:])
            f.close()
            print("file was recieved")
        else:
            print(msg)

if __name__ == '__main__':
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_host   = socket.gethostname()
    ip       = socket.gethostbyname(s_host)
    s_PORT   = 9992

    print("Your IP :",ip)
    s_host = input('Enter server\'s IP address:')
    name = input('Enter your name:')
    c_socket.connect((s_host,s_PORT))

    c_socket.sendall(name.encode())
    server_name = c_socket.recv(1024)
    server_name = server_name.decode()
    print('Connected with',server_name)
    message = "get_list"
    c_socket.sendall(message.encode())
    start_new_thread(writing,())
    while True:
        message = input()
        if message == "file" :
            recieve=input("Enter the names of recivers with space : ")
            file = input("Enter the path to the file here : ")
            filename = os.path.basename(file)
            f = open(file,'r')
            message = f.read()
            message= "file"+ " "+recieve+" "+":"+" "+filename+","+ message
        c_socket.sendall(message.encode())
        if message =='quit':
            break
        c_socket.send(message.encode())
        data = c_socket.recv(1024)
        
    c_socket.close()

    


