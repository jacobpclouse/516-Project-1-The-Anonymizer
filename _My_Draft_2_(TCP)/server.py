'''
 This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
 
 Questions: 
 1) I am getting this error on longer files that I want to convert: OSError: [Errno 9] Bad file descriptor
    I had issues with longer files as well as single line files
 '''

import socket
import sys # WILL NEED TO GET RID OF THIS LATER


jakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
jakeServer.bind((socket.gethostname(), 12000))

# shows server is up and running
print("The server is ready to receive")

# buffer set to 5
jakeServer.listen(5)

while True:
    clientSocket, address = jakeServer.accept()
    print(f"Connection from {address} has been established.")

    #---

    uncensoredPhrase = clientSocket.recv(2048).decode()
    print(f"the uncensored phrase is {uncensoredPhrase}")

    #Creating the data to send back to client
    toClient = f"THE RETURN PHRASE IS {uncensoredPhrase}"
    clientSocket.send(toClient.encode())
    
    #---


    jakeServer.close()
