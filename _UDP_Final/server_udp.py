# THIS USES PYTHON Python 3.8.10

'''
 This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
 
 Questions: 
 1) For the get function, is the string specified after the name of the file that you want to output it as?
 2) This program is very linear, it expects things in a specific order (ie: put, keyword, get) is that ok?
 3) I expect a port number on input of function, should i have contingency port if that is not entered? 
        Should we assume that you will only test port numbers? or will you try and cause an error by leaving it blank/enterning letters?

 4) I'm not getting full length back the second time (it gives me full message first time, but only like 2/3 on second) Why?
 5) How do I quit out of a program at any time?  

 6) For some reason, sometimes I need to put in my computers hostname (ie: SHODAN) instead of IP, why? It worked with the previous copy, but not here for some reason (specifically UDP) 
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

def chunkerFunction(string):

    #-------------------
    # chunker Variables: 
    #-------------------

    # getting length of string
    stringLength = len(string)
    print(f"Length of String: {stringLength} characters")

    # determining the target size (ie: this will be 1000 for udp)
    byteSize = 10

    # setting a counter equal to length, will decriment as chunks are written
    lengthLeft = stringLength

    # setting start position variable, will incriment up
    startCut = 0

    # setting end cut (exclusive), will incriment up
    endCut = startCut + byteSize


    #---------------
    # chunker Logic:
    #---------------

    # implimenting a sort of do while loop
    # https://www.educative.io/edpresso/how-to-emulate-a-do-while-loop-in-python
    while True:
        # printing out chunk equal to byte size
        print(string[startCut:endCut])
        arrayToSend.append(string[startCut:endCut])

        # Incrimenting startCut and endCut by byteSize
        startCut += byteSize
        endCut += byteSize

        # Decrimenting lengthLeft
        lengthLeft -= byteSize

        # If lengthLeft is less than or equal to byteSize, just print out what is left and end it
        if(lengthLeft <= byteSize):
            print(string[startCut:])
            arrayToSend.append(string[startCut:])
            break


# -----
# Socket Port and IP 

SocketIP = returnIP()
SocketIP = socket.gethostname()
print(SocketIP)
SocketPortNumber = returnPort()
print(SocketPortNumber)



jakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeServer.bind((SocketIP, SocketPortNumber))


# Variables
serverNeedToCensor = ''
serverSecretPhrase = ''

# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []
chunkBookmark = 0

# added
serverOriginalFileName = ''
serverCensoredName = ''

serverNeedToCensor = ''

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
    #f = open("myfile.txt", "x")
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

    # check to see if serverKeywordArray[1] exits with if statement
    serverKeywordFileName = serverKeywordArray[1]
    print(f"Keyword Filename: {serverKeywordFileName}")

    # creating string to replace target phrase with
    serverReplacementString = myFindTargetString(serverSecretPhrase)
    print(serverReplacementString)

    # opening file
    # https://docs.python.org/3/library/functions.html#open
    textToChange = open(f"{serverKeywordFileName}_")
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
    
    #f = open(f"{serverCensoredName}", "x")
    with open(f"{serverCensoredName}", 'w') as f:
        print(serverCensoredOutput, file=f)

# ----


    
    # send response back to client
    # Sending back name of the new censored file
    messageRecieved = f"Server response: File {serverKeywordFileName} has been anonymized. Output file is {serverCensoredName}"
    clientSocket.send(messageRecieved.encode())

    # maybe send as header?
    #clientSocket.send(serverCensoredName.encode())
    
    # -----------
    # GET COMMAND
    # -----------

    # Recieving get command and checking to see if what the anon file is
    serverGetRequest = clientSocket.recv(2048).decode()

    print(serverGetRequest)
    print(f"Get Request Recieved: Sending back censored output")

    print(f"The length of string output: {len(serverCensoredOutput)}")
    #serverGetOutput = "Your Request was flawed"

    # if the requested filename is the same as the anonymized file,
    # then move contents to a string
    # if serverGetRequest == serverCensoredName:
    #     serverGetOutput = open(f"{serverCensoredName}")
    #     serverFinalText = textToChange.read()
    #     textToChange.close()
    textToChange = open(serverCensoredName)
    serverFinalText = textToChange.read()
    print(f"Length of Text to Send to Client: {len(serverFinalText)}")
    textToChange.close()

        
    clientSocket.send(serverFinalText.encode())
    #clientSocket.send(serverFinalText.encode("utf"))
    
   

