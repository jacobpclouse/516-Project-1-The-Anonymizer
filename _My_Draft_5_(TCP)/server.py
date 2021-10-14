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
    clientSocket, clientAddress = jakeServer.accept()
    print(f"Connection from {clientAddress} has been established.")

    # ---
    # Accepting String that needs to be censored from client
    serverNeedToCensor = clientSocket.recv(2048).decode()
    print(f"the uncensored phrase is {serverNeedToCensor}")

    # ---
    # Accepting the Top Secret Word to censor from client
    serverSecretPhrase = clientSocket.recv(2048).decode()
    print(f"the uncensored phrase is {serverSecretPhrase}")

    # ---
    # Accepting the replacement character to censor from client
    serverReplacementChar = clientSocket.recv(2048).decode()
    print(f"the uncensored phrase is {serverReplacementChar}")

    # ---
    # Displaying output
    print(
        f"RECIEVED {serverNeedToCensor, serverSecretPhrase, serverReplacementChar} FROM {clientAddress}")

   # --

    # Gets length of string and creates the character to replace it with
    replacementString = ''

    for letters in serverSecretPhrase:
        replacementString += serverReplacementChar

    print(f"The Replacement string will be {replacementString}")

# --

    # Doing find and replace
    # from https://www.geeksforgeeks.org/python-string-replace/
    censoredOutput = serverNeedToCensor.replace(
        serverSecretPhrase, replacementString)
    # print(censoredOutput)


    # Creating the data to send back to client
    clientSocket.send(censoredOutput.encode())

    # ---
