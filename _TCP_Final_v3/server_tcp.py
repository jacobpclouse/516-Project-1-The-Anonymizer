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

# Functions

# Gets length of string and creates the character to replace it with
def myFindTargetString(targetPhase):
    replacementString = ''
    replacementChar = 'X'
    for letters in targetPhase:
        replacementString += replacementChar
    return replacementString



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

    # -----------
    # PUT COMMAND
    # -----------


    # Accepting original filename from client
    # created new filename from original
    serverOriginalFileName = clientSocket.recv(2048).decode()
    serverCensoredName = "Anon" + serverOriginalFileName

    # Accepting String that needs to be censored from client
    # serverNeedToCensor = clientSocket.recv(2048).decode("utf-8")
    serverNeedToCensor = clientSocket.recv(65527).decode()
    print(f"String that needs to be censored is: {serverNeedToCensor}")
    print(f"The length of the file is: {len(serverNeedToCensor)}")



    # Output sting to file
    # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    with open(f'{serverOriginalFileName}_', 'w') as f:
        print(serverNeedToCensor, file=f)

    # send response back to client
    messageRecieved = "Server response: File Uploaded"
    clientSocket.send(messageRecieved.encode())

    # cleaning up
    messageRecieved = ''

    # ---------------
    # KEYWORD COMMAND
    # ---------------

    # Accepting the word to censor from client
    # AND target file's filename from client
    serverKeywordData = clientSocket.recv(2048).decode()
    serverKeywordArray = serverKeywordData.split(' ', 1)

    serverSecretPhrase = serverKeywordArray[0]
    print(f"Top Secret Word to censor is: {serverSecretPhrase}")

    serverKeywordFileName = serverKeywordArray[1]
    print(f"Keyword Filename: {serverKeywordFileName}")


    # opening file
    # https://docs.python.org/3/library/functions.html#open
    textToChange = open(f"{serverKeywordFileName}_")
    serverWholeFileToString = textToChange.read()
    textToChange.close()


    # Anonymize Logic here
    # creating string to replace target phrase with
    serverReplacementString = myFindTargetString(serverSecretPhrase)
    print(serverReplacementString)

    # send response back to client
    # Sending back name of the new censored file
    messageRecieved = f"Server response: File {serverKeywordFileName} has been anonymized. Output file is {serverCensoredName}"
    clientSocket.send(messageRecieved.encode())

    


#     # Accepting file path from client to ensure that it is the same as the one from the put command
# # ---
#     # Displaying output
#     print(
#         f"RECIEVED {serverNeedToCensor, serverSecretPhrase} FROM {clientAddress}")

#    # --

#     # Gets length of string and creates the character to replace it with
#     replacementString = ''
#     serverReplacementChar = 'X'

#     for letters in serverSecretPhrase:
#         replacementString += serverReplacementChar

#     print("The Replacement string will be: ")
#     print(replacementString)


# # --

#     # Doing find and replace
#     # from https://www.geeksforgeeks.org/python-string-replace/
#     censoredOutput = serverNeedToCensor.replace(
#         serverSecretPhrase, replacementString)
#     print(censoredOutput)


#     # ---
#     # Get command - will send after recieving initiation
#     # 
#     serverGetRequest = clientSocket.recv(2048).decode()
#     print(f"Get Request Recieved: Sending back censored output")



#     # Creating the data to send back to client
#     clientSocket.send(censoredOutput.encode())
    

#     # ---
