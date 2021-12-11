from _thread import *
import threading
import socket
import time
import sys
import base64
from datetime import datetime
import os 
import imghdr
from PIL import Image
import io
import re
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = bytes(data,"ASCII")
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

def writing():
    while True:
        msg=c_socket.recv(1024)
        msg=msg.decode()
        if msg[:4]=="file":
            div=msg.index(",")
            filename=msg[4:div]
            if msg[div+1]!='^':
                f= open(filename,"w")
                f.write(msg[div+1:])
                f.close()
            else:
                img = io.BytesIO(decode_base64(msg[div+2:]))
                pilimage = Image.open(img)
                pilimage = pilimage.save(filename)
            print("A file name {} has recieved".format(filename))
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

    c_socket.send(name.encode())
    server_name = c_socket.recv(1024)
    server_name = server_name.decode()
    print('Connected with ',server_name)
    message = "get_list"
    c_socket.send(message.encode())
    start_new_thread(writing,())
    while True:
        message = input()
        if message == "file" :
            recieve=input("enter the names of recivers with space : ")
            file = input("Enter the path to the file here : ")
            if imghdr.what(file) == None:
                 f = open(file,'r')
                 message = f.read()
            else:
                f= open(file,"rb")
                message="^"+base64.b64encode(f.read()).decode('ASCII')
                print(len(message))
            filename = os.path.basename(file)
            message= "file"+ " "+recieve+" "+":"+" "+filename+','+ message
        if message =='quit':
            break
        c_socket.send(message.encode())
        
    c_socket.close()
