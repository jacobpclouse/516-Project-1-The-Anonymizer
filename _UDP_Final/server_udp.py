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

 6) Why are the '\\n' being stored instead of the carriage returns? I don't know how to fix that in transit!
 '''

# Import libraries
import socket
import sys


# --
# Functions

# Gets length of string and creates the character to replace it with
def myFindTargetString(targetPhase):
    replacementString = ''
    replacementChar = 'X'
    for letters in targetPhase:
        replacementString += replacementChar
    return replacementString



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

#SocketIP = returnIP()
SocketIP = socket.gethostname()
print(SocketIP)
SocketPortNumber = returnPort()
print(SocketPortNumber)



#jakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
#jakeServer.bind((SocketIP, SocketPortNumber))
# ---

jakeServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
jakeServerUDP.bind((SocketIP, SocketPortNumber))

# --


# Variables
serverNeedToCensor = ''
serverSecretPhrase = ''

# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []
chunkBookmark = 0

# added
serverNeedToCensorLength = ''
serverNeedToCensorLengthArray = ['', '']

serverOriginalFileName = ''
serverCensoredName = ''

serverNeedToCensor = ''

serverKeywordData = 'default value'
serverKeywordFileName = ''

serverGetRequest = ''

serverFinalText = ''

# ---
# Program logic
# ---


# shows server is up and running
print("The server is ready to receive")


# clientSocket, clientAddress = jakeServer.accept()
# going to get data from client, loop until manually stoped
while True:

    # Server prints this if it has been successfully created
    print(f'The server is ready to receive on Hostname: {SocketIP}, Port: {SocketPortNumber}')

#     # -----------
#     # PUT COMMAND
#     # -----------


    # Need to accept and print out length of incoming string
    # Decoding and pushing it through to array, then displaying
    serverNeedToCensorLength, clientAddress = jakeServerUDP.recvfrom(2048)
    serverNeedToCensorLength = serverNeedToCensorLength.decode()
    serverNeedToCensorLengthArray = (serverNeedToCensorLength).split(':', 1)
    print(serverNeedToCensorLengthArray)
    print(f"According to client, The length of the file is: {serverNeedToCensorLengthArray[1]}")


    # find out how many chunks of 1000 you will send, ceiling it
    # https://www.geeksforgeeks.org/floor-ceil-function-python/
    lengthOfChunk = 1000
    loopsOfChunk = float(serverNeedToCensorLengthArray[1]) / lengthOfChunk
    loopsOfChunkTrunk = int(loopsOfChunk)
    print(loopsOfChunk)
    print(loopsOfChunkTrunk)

    #if original value and truncated value are not the same, we will increase truncated value by 1
    if loopsOfChunk != loopsOfChunkTrunk:
        loopsOfChunk = loopsOfChunkTrunk + 1
        # this will be how many loops we will have to send
    print(f"Expecting {loopsOfChunk} chunks")


    # Creating String to write recive from 
    serverNeedToCensor = ''

    # Going to recieve 
    currentChunkIndex = 0
    serverAckOutbound = "Chunk has been recieved!"

    while currentChunkIndex < loopsOfChunk:
        print(f"On Array Section {currentChunkIndex}")


        # Recieving string in 1000 byte incriments
        serverNeedToCensor, clientAddress = jakeServerUDP.recvfrom(65527)
        inboundString = serverNeedToCensor.decode("utf-8")
        #print(serverNeedToCensor)

        # Sending ACK
        jakeServerUDP.sendto(serverAckOutbound.encode(), clientAddress)

        # incriment
        #currentChunkIndex += 1    


        # Server Side File Storage
        ServerSideFileName = "ServerSideFile__" + str(loopsOfChunk) #+ ".txt"


        if currentChunkIndex == 0:

            # Creating File
            # Overwrite previous file with same name (so we don't accidentally append to it)
            with open(f"{ServerSideFileName}", 'w') as f:
                print(inboundString, file=f)

            # cleanup
            inboundString = ''
                
            
        else:

            #Writing to file
        # https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
            with open(f"{ServerSideFileName}", 'a') as f:
                print(inboundString, file=f)
        

        # incriment
        currentChunkIndex += 1 

        # cleanup
        inboundString = ''

        


    # Send Fin String to client
    finMessageToClient = 'Progress To Next Step'

    # checking to see if the number of chunks we got was equal to the number we expected
    if currentChunkIndex == loopsOfChunk:
        print("Number of Chunks Recieved == Number of Chunks Expected")
    
        jakeServerUDP.sendto(finMessageToClient.encode(), clientAddress)


    ##TIMEOUT - Need to put an else here if the number of packets doesn't match up


    # ---------------
    # KEYWORD COMMAND
    # ---------------

    # Accepting the word to censor from client
    # AND target file's filename from client

    serverKeywordData, clientAddress = jakeServerUDP.recvfrom(2048)
    serverKeywordArray = (serverKeywordData.decode()).split(' ', 1)

    # Getting Phase to Censor
    serverSecretPhrase = serverKeywordArray[0]
    print(f"Top Secret Word to censor is: {serverSecretPhrase}")


    # Getting Original Name of file, will use to rename new text
            # check to see if serverKeywordArray[1] exits with if statement
    serverKeywordFileName = serverKeywordArray[1]
    print(f"Keyword Filename: {serverKeywordFileName}")
    serverCensoredName = "Anon" + str(serverKeywordFileName) + "_UDP"
    print(serverCensoredName)

    # creating string to replace target phrase with
    serverReplacementString = myFindTargetString(serverSecretPhrase)
    print(f"Replacement String will be: {serverReplacementString}")


    # opening new anon file
    # https://docs.python.org/3/library/functions.html#open
    textToChange = open(f"{ServerSideFileName}")
    serverWholeFileToString = textToChange.read()
    textToChange.close()


# # --------------------------##
#      Anonymize Logic here    #
# # --------------------------##


    # Doing find and replace
    # from https://www.geeksforgeeks.org/python-string-replace/
    serverCensoredOutput = serverWholeFileToString.replace(
        serverSecretPhrase, serverReplacementString)

    
    # Overwriting any previous file with the same name
    f = open(f"{serverCensoredName}", "w")

    # Output sting to file
    # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    
    with open(f"{serverCensoredName}", 'a') as f:
        print(serverCensoredOutput, file=f)


    # finishing up and Sending response back to client
    print("File Written Successfully")
# # ----










# ---------
#     # Accepting original filename from client
#     # created new filename from original
#     serverOriginalFileName, clientAddress = jakeServerUDP.recvfrom(2048)
#     serverCensoredName = "Anon" + serverOriginalFileName

#     # Accepting String that needs to be censored from client
#     serverNeedToCensor, clientAddress = jakeServerUDP.recvfrom(65527)
#     print(f"String that needs to be censored is: {serverNeedToCensor}")
#     print(f"The length of the file is: {len(serverNeedToCensor)}")



#     # Output sting to file
#     # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
#     #f = open("myfile.txt", "x")
#     with open(f'{serverOriginalFileName}_', 'w') as f:
#         print(serverNeedToCensor, file=f)

#     # send response back to client
#     messageRecieved = "Server response: File Uploaded"
#     ##clientSocket.send(messageRecieved.encode())
#     jakeServerUDP.sendto(messageRecieved.encode(), clientAddress)

#     # cleaning up
#     messageRecieved = ''

#     # ---------------
#     # KEYWORD COMMAND
#     # ---------------

#     # Accepting the word to censor from client
#     # AND target file's filename from client

#     serverKeywordData, clientAddress = jakeServerUDP.recvfrom(2048)
#     serverKeywordArray = (serverKeywordData.decode()).split(' ', 1)

#     serverSecretPhrase = serverKeywordArray[0]
#     print(f"Top Secret Word to censor is: {serverSecretPhrase}")

#     # check to see if serverKeywordArray[1] exits with if statement
#     serverKeywordFileName = serverKeywordArray[1]
#     print(f"Keyword Filename: {serverKeywordFileName}")

#     # creating string to replace target phrase with
#     serverReplacementString = myFindTargetString(serverSecretPhrase)
#     print(serverReplacementString)

#     # opening file
#     # https://docs.python.org/3/library/functions.html#open
#     textToChange = open(f"{serverKeywordFileName}_")
#     serverWholeFileToString = textToChange.read()
#     textToChange.close()

# # ----
#     # Anonymize Logic here
# # ----

#     # Doing find and replace
#     # from https://www.geeksforgeeks.org/python-string-replace/
#     serverCensoredOutput = serverWholeFileToString.replace(
#         serverSecretPhrase, serverReplacementString)

#     # Output sting to file
#     # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    
#     #f = open(f"{serverCensoredName}", "x")
#     with open(f"{serverCensoredName}", 'w') as f:
#         print(serverCensoredOutput, file=f)

# # ----


    
#     # send response back to client
#     # Sending back name of the new censored file
#     messageRecieved = f"Server response: File {serverKeywordFileName} has been anonymized. Output file is {serverCensoredName}"
#     ##clientSocket.send(messageRecieved.encode())
#     jakeServerUDP.sendto(messageRecieved.encode(), clientAddress)

#     # maybe send as header?
#     #clientSocket.send(serverCensoredName.encode())
    
#     # -----------
#     # GET COMMAND
#     # -----------

#     # Recieving get command and checking to see if what the anon file is
#     ##serverGetRequest = clientSocket.recv(2048).decode()
#     serverGetRequest, clientAddress = jakeServerUDP.recvfrom(2048)

#     print(serverGetRequest)
#     print(f"Get Request Recieved: Sending back censored output")

#     print(f"The length of string output: {len(serverCensoredOutput)}")
#     #serverGetOutput = "Your Request was flawed"

#     # if the requested filename is the same as the anonymized file,
#     # then move contents to a string
#     # if serverGetRequest == serverCensoredName:
#     #     serverGetOutput = open(f"{serverCensoredName}")
#     #     serverFinalText = textToChange.read()
#     #     textToChange.close()
#     textToChange = open(serverCensoredName)
#     serverFinalText = textToChange.read()
#     print(f"Length of Text to Send to Client: {len(serverFinalText)}")
#     textToChange.close()


#     #Send back to user    
#     ##clientSocket.send(serverFinalText.encode())
#     jakeServerUDP.sendto(serverFinalText.encode(), clientAddress)
    
   

