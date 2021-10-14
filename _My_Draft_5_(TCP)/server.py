'''
 This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
 
 Questions: 
 1) I am getting this error on longer files that I want to convert: OSError: [Errno 9] Bad file descriptor
    I had issues with longer files as well as single line files (doesn't look like size)
    Does it have to do with timeout not being set?
 '''

import socket

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
   # Accepting String that needs to be censored from client
   serverUncensoredPhrase = clientSocket.recv(2048).decode()
   print(f"the uncensored phrase is {serverUncensoredPhrase}")


   #---
   # Accepting the Top Secret Word to censor from client
   serverTopSecretPhrase = clientSocket.recv(2048).decode()
   print(f"the uncensored phrase is {serverTopSecretPhrase}")


   #---
   # Accepting the replacement character to censor from client
   serverReplacementChar = clientSocket.recv(2048).decode()
   print(f"the uncensored phrase is {serverReplacementChar}")


   #---

   

   #Creating the data to send back to client
   toClient = f"THE RETURN PHRASE IS {uncensoredPhrase}"
   clientSocket.send(toClient.encode())
    
   #---



