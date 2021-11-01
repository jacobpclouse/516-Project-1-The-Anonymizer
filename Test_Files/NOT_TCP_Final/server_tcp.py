'''
 This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
 
 Questions: 
 1) I am getting this error on longer files that I want to convert: OSError: [Errno 9] Bad file descriptor
    I had issues with longer files as well as single line files (doesn't look like size)
    Does it have to do with timeout not being set?
 '''
# Socket Stuff
import socket

SocketIP = socket.gethostname()
SocketPortNumber = int(input("Give me a port Number: "))

jakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeServer.bind((SocketIP, SocketPortNumber))


# Variables
serverNeedToCensor = ''
serverSecretPhrase = ''
# hasGetBeenRecieved = False

# ---

# Functions



# ---

# Program logic
# shows server is up and running
print("The server is ready to receive")

# buffer set to 5
jakeServer.listen(5)

# clientSocket, clientAddress = jakeServer.accept()
# going to get data from client, loop until manually stoped
while True:
    clientSocket, clientAddress = jakeServer.accept()
    print(f"Connection from {clientAddress} has been established.")


    # ---
    # Put command 
    # Accepting String that needs to be censored from client
    serverNeedToCensor = clientSocket.recv(2048).decode()
    print(f"String that needs to be censored is: {serverNeedToCensor}")

    # ---
    # Keyword command 
    # Accepting the Top Secret Word to censor from client
    serverSecretPhrase = clientSocket.recv(2048).decode()
    print(f"Top Secret Word to censor is: {serverSecretPhrase}")

# ---
    # Displaying output
    print(
        f"RECIEVED {serverNeedToCensor, serverSecretPhrase} FROM {clientAddress}")

   # --

    # Gets length of string and creates the character to replace it with
    replacementString = ''
    serverReplacementChar = 'X'

    for letters in serverSecretPhrase:
        replacementString += serverReplacementChar

    print("The Replacement string will be: ")
    print(replacementString)


# --

    # Doing find and replace
    # from https://www.geeksforgeeks.org/python-string-replace/
    censoredOutput = serverNeedToCensor.replace(
        serverSecretPhrase, replacementString)
    print(censoredOutput)


    # ---
    # Get command - will send after recieving initiation
    # 
    serverGetRequest = clientSocket.recv(2048).decode()
    print(f"Get Request Recieved: Sending back censored output")
    # hasGetBeenRecieved = True


    # Creating the data to send back to client
    clientSocket.send(censoredOutput.encode())
    

    # ---
