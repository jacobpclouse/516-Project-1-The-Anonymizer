'''
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1235))
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection {clientsocket} from {address} has been established.")
    clientsocket.send(bytes("Hey there!!!","utf-8"))
    clientsocket.close()

    
 This was taken from https://pythonprogramming.net/sockets-tutorial-python-3/ '''


import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1235))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    
    msg = "Welcome to the Server"
    print(f'{len(msg):<{HEADERSIZE}}' + msg)

    clientsocket.send(bytes("Welcome to the server!", "utf-8"))
