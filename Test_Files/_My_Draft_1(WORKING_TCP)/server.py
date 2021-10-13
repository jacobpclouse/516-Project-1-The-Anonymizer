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

#This is done with TCP, listen and accept error out with UDP
jakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#jakeServer.bind((socket.gethostname(), 12000))
jakeServer.bind((socket.gethostname(), 12000))
print("The server is ready to receive")
jakeServer.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientSocket, address = jakeServer.accept()
    #print(f"Connection from {address} has been established.")

    fromClient = clientSocket.recv(2048).decode()
    print(f"the Number is {fromClient}")
    toClient = f"The Number you gave us is {fromClient}"
    #toClient = int(fromClient) + 1

    clientSocket.send(toClient.encode())

    #clientsocket.send(bytes("Hey there!!!","utf-8"))
    jakeServer.close()
