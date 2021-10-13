''' 
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1235))

msg = s.recv(1024)
print(msg.decode("utf-8"))

This was taken from https://pythonprogramming.net/sockets-tutorial-python-3/ '''


import socket
from typing_extensions import TypeGuard

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1235))

while True: 

    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        
        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msglen:
           print("full msg recvd") 
           print(full_msg[HEADERSIZE:])
           new_msg = True

    print(full_msg)