'''
 This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
 
 Questions: 
 1) For the get function, is the string specified after the name of the file that you want to output it as?
 2) This program is very linear, it expects things in a specific order (ie: put, keyword, get) is that ok?
 3) I expect a port number on input of function, should i have contingency port if that is not entered? 
        Should we assume that you will only test port numbers? or will you try and cause an error by leaving it blank/enterning letters?

        
 '''

# Import libraries
import socket
import sys



# importing Command line arguments - for IP and port numbers
# https://cs.stanford.edu/people/nick/py/python-main.html


def returnIP():
    incomingIP = sys.argv[1]
    return incomingIP


def returnPort():
    incomingPort = int(sys.argv[2])
    return incomingPort


#SocketIP = socket.gethostname()
SocketIP = returnIP()
print(SocketIP)
SocketPortNumber = returnPort()
print(SocketPortNumber)



jakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeServer.bind((SocketIP, SocketPortNumber))


# Variables
serverNeedToCensor = ''
serverSecretPhrase = ''

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

    # PUT: accepting file path so that we can compair to keyword path later
    serverFilePathFromClient = clientSocket.recv(2048).decode()
    print(f"PUT: File Path has been stored: {serverFilePathFromClient}")


    # ---
    # Keyword command 
    # Accepting the Top Secret Word to censor from client
    serverSecretPhrase = clientSocket.recv(2048).decode()
    print(f"Top Secret Word to censor is: {serverSecretPhrase}")

    # KEYWORD: accepting file path so that we can compair to keyword path later
    serverFilePathKeyword = clientSocket.recv(2048).decode()
    print(f"KEYWORD: File Path has been stored: {serverFilePathKeyword}")



    # Accepting file path from client to ensure that it is the same as the one from the put command
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



    # Creating the data to send back to client
    clientSocket.send(censoredOutput.encode())
    

    # ---
