from _thread import *
import threading
import socket
import time
import sys
from datetime import datetime


def writing():
    while True:
        msg = c_socket.recv(1024)
        print(msg.decode())


if __name__ == '__main__':
    # Creating server socket
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_host = socket.gethostname()
    ip = socket.gethostbyname(s_host)
    s_PORT = 9992

    print("Your IP :", ip)
    s_host = input('Enter friend\'s IP address:')
    name = input('Enter your name:')
    c_socket.connect((s_host, s_PORT))

    c_socket.sendall(name.encode())
    server_name = c_socket.recv(1024)
    server_name = server_name.decode()
    print('Connected with ', server_name)
    start_new_thread(writing, ())
    while True:
        # print(server_name,":",message)
        message = input()
        if message == 'quit':
            break
        c_socket.send(message.encode())
        # data = c_socket.recv(1024)

    c_socket.close()
