from _thread import *
import threading
import socket
import time
import sys
from datetime import datetime

MAX_CLIENTS = 10
client_list = []
client_names = []
forbidden_list = []

my_lock = threading.Lock()
password = "CS3530" # Change password here.


def password_check(conn, name, addr):
    key = 0
    trail = 1
    if addr in forbidden_list:
        print(addr, " again tried to connect to the server")
        msg = "Incorrect password"
        msg = msg.encode()
        conn.send(msg)
        return 0
    while trail < 4 and key == 0:
        check = "Enter the password trail(" + str(trail) + "/3) :"
        conn.send(check.encode())
        message = conn.recv(1024)
        if message == password.encode():
            key = 1
            msg = "Connection successful"
            print("Connection with " + name + " was successful")
            conn.send(msg.encode())
            break
        trail = trail + 1
    if trail == 4:
        print(str(name) + " tried to connect with wrong password")
        forbidden_list.append(addr)
        msg = "Incorrect password"
        conn.send(msg.encode())
    return key


def threaded(conn, name, addr):
    key = password_check(conn, name, addr)
    while True:
        if key == 0:
            break
        else:
            print("Clients available are: " + " ".join(client_names))
        message = conn.recv(1024)
        if not message:
            print(name + " connection closed")
            break
        command = message.decode().split(" ")
        if command[0] == "get_list":
            friends = client_names.copy()
            friends.remove(name)
            msg = "friends in the room : " + " ".join(friends)
            msg = msg.encode()
            conn.send(msg)

        elif command[0] == "send" and command[1] == "all" and len(command) >= 3:
            for (names, connec) in client_list:
                if connec != conn:
                    msg = name + " :" + " ".join(command[2:])
                    connec.send(msg.encode())

        elif command[0] == "send":
            div = command.index(":")
            list_of_c = command[1:div]
            msg = name + " :" + " ".join(command[div + 1:])
            for (names, connec) in client_list:
                if names in list_of_c:
                    connec.send(msg.encode())
                    list_of_c.remove(names)
        elif command[0] == "file":
            div = command.index(":")
            list_of_c = command[1:div]
            msg = "file" + " ".join(command[div + 1:])
            for (names, connec) in client_list:
                if names in list_of_c:
                    connec.send(msg.encode())
                    list_of_c.remove(names)
    conn.close()
    client_list.remove((name, conn))


if __name__ == '__main__':

    s_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating socket
    s_hostname = socket.gethostname()  # retrieving hostname
    s_ip = socket.gethostbyname(s_hostname)  # get ip of host
    port = 9992
    s_soc.bind((s_ip, port))  # binding host to port
    print("IP of server :", s_ip)
    s_name = input('Enter name of Server:')
    s_soc.listen(MAX_CLIENTS)
    print("In Listen mode..")

    while True:
        conn, add = s_soc.accept()  # accepting connection
        c_message = conn.recv(1024)
        name_of_client = c_message.decode()
        msg = "Welcome your friend " + name_of_client + " to the  party"
        msg = msg.encode()
        for (name, conect) in client_list:
            conect.send(msg)
        print(name_of_client, " is trying to connect")
        client_list.append((name_of_client, conn))
        client_names.append(name_of_client)
        conn.send(s_name.encode())
        start_new_thread(threaded, (conn, name_of_client, add[0]))
    s_soc.close()
