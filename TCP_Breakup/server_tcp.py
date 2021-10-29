# THIS USES PYTHON Python 3.8.10

'''
 This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
 

 1) It looks like I'm running out of buffer space (line 147 being overwritten)
 '''

# Import libraries
from os import pread
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

# ---

# Taking the values for IP and Port from command line arguments

SocketIP = returnIP()
print(SocketIP)
SocketPortNumber = returnPort()
print(SocketPortNumber)


# Creating & Binding Server to Specified IP & Port

jakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeServer.bind((SocketIP, SocketPortNumber))


# ---


# Variables
serverNeedToCensor = ''
serverSecretPhrase = ''

# # added
serverStartup = "The server is ready to receive"

serverOriginalFileName = ''
serverCensoredName = ''

serverKeywordData = 'default value'
serverKeywordFileName = ''

serverGetRequest = ''

serverFinalText = ''

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
print(serverStartup)

# buffer set to 20
jakeServer.listen(5)


# going to get data from client, loop until manually stoped
while True:
    serverOriginalFileName = ''
    # Displaying connection from client
    clientSocket, clientAddress = jakeServer.accept()
    print(f"Connection from {clientAddress} has been established.")


    # -----------
    # PUT COMMAND
    # -----------



    # Accepting original filename from client
    # created new filename from original
    serverOriginalFileName = clientSocket.recv(2048).decode()
    serverCensoredName = "Anon" + serverOriginalFileName
# ---

    # getting number of loops that are incoming
    serverLoopsOfChunk  = clientSocket.recv(2048).decode()
    print(f"Number Of Chunks To Expect From Client: {serverLoopsOfChunk}")
    
    
    # Sending Ack back
    clientSocket.send(serverStartup.encode())
    print("Length Ack Sent!")
# ---
# recieving incoming chunks:

    # Creating String to write recive from 
    serverNeedToCensor = ''

    # Going to recieve 
    currentChunkIndex = 0
    

    # Server Side File Storage
    ServerSideFileName = f"{serverOriginalFileName}_"


    while currentChunkIndex < int(serverLoopsOfChunk):
        print(f"On String Section Section {currentChunkIndex}")
        print(f"Need to get to {int(serverLoopsOfChunk)}")

        # Recieving string in 1000 byte incriments
        #serverNeedToCensor, clientAddress = jakeServer.accept()
        #serverNeedToCensor, clientAddress = jakeServer.recv(65000)
        serverNeedToCensor  = clientSocket.recv(65000)
        inboundString = serverNeedToCensor.decode("utf-8")
        print(inboundString)

        # creating ACK
        serverAckOutbound =  f"Chunk {currentChunkIndex} has been recieved!"


        if currentChunkIndex == 0:

            # Creating File
            # Overwrite previous file with same name (so we don't accidentally append to it)
            with open(f"{serverOriginalFileName}_", 'w') as f:
                print(inboundString, file=f)

            print("1st statement")
            # cleanup
            inboundString = ''
            currentChunkIndex += 1 

            # Sending Ack
            clientSocket.send(serverAckOutbound.encode())    
            
        else:

            #Writing to file
        # https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
            with open(f"{serverOriginalFileName}_", 'a') as f:
                print(inboundString, file=f)
        
            print("2nd Statement")
            # incriment
            currentChunkIndex += 1 

            # cleanup
            inboundString = ''

            # Sending Ack
            clientSocket.send(serverAckOutbound.encode())

     # Sending ACK
    clientSocket.send(serverAckOutbound.encode())

    print("Done with Recieving!")


# ---
    
    # Open file, write to string, get length of string, compair!
    
    
    # Accepting String that needs to be censored from client
    #serverNeedToCensor = clientSocket.recv(100000).decode()
    
    # print(f"String that needs to be censored is: {serverNeedToCensor}")
    # print(f"The length of the file is: {len(serverNeedToCensor)}")



    # # Output sting to file
    # # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    # with open(f'{serverOriginalFileName}_', 'w') as f:
    #     print(serverNeedToCensor, file=f)

    # send response back to client
    # messageRecieved = "Server response: File Uploaded"
    # clientSocket.send(messageRecieved.encode())

    # cleaning up
    # messageRecieved = ''

    # ---------------
    # KEYWORD COMMAND
    # ---------------

    # Accepting the word to censor from client
    # AND target file's filename from client
    serverKeywordData = clientSocket.recv(2048).decode()
    serverKeywordArray = serverKeywordData.split(' ', 1)

    serverSecretPhrase = serverKeywordArray[0]
    print(f"Top Secret Word to censor is: {serverSecretPhrase}")

    # check to see if serverKeywordArray[1] exits with if statement
    serverKeywordFileName = serverKeywordArray[1]
    print(f"Keyword Filename: {serverKeywordFileName}")

    # creating string to replace target phrase with
    serverReplacementString = myFindTargetString(serverSecretPhrase)
    print(serverReplacementString)

    # opening file
    # https://docs.python.org/3/library/functions.html#open
    textToChange = open(f"{serverOriginalFileName}_")
    serverWholeFileToString = textToChange.read()
    textToChange.close()

# ----
    # Anonymize Logic here
# ----

    # Doing find and replace
    # from https://www.geeksforgeeks.org/python-string-replace/
    serverCensoredOutput = serverWholeFileToString.replace(
        serverSecretPhrase, serverReplacementString)

    # Output sting to file
    # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    
    with open(f"{serverCensoredName}", 'w') as f:
        print(serverCensoredOutput, file=f)

# ----


    
    # send response back to client
    # Sending back name of the new censored file
    messageRecieved = f"Server response: File {serverKeywordFileName} has been anonymized. Output file is {serverCensoredName}"
    clientSocket.send(messageRecieved.encode())
    
    # -----------
    # GET COMMAND
    # -----------

    # Recieving get command and checking to see if what the anon file is
    serverGetRequest = clientSocket.recv(2048).decode()

    print(serverGetRequest)
    print(f"Get Request Recieved: Sending back censored output")

    print(f"The length of string output: {len(serverCensoredOutput)}")

    textToChange = open(serverCensoredName)
    serverFinalText = textToChange.read()
    print(f"Length of Text to Send to Client: {len(serverFinalText)}")
    textToChange.close()

    # Sending final text back to client
    clientSocket.send(serverFinalText.encode())

    # Cleanup
    serverWholeFileToString = ''
    serverNeedToCensor = ''

    serverOriginalFileName = ''
    serverCensoredName = ''

    serverKeywordData = 'default value'
    serverKeywordFileName = ''

    serverGetRequest = ''

    serverFinalText = ''
    serverSecretPhrase = ''

    messageRecieved = ''