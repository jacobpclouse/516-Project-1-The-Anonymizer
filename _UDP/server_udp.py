# THIS USES PYTHON Python 3.8.10
# This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
# No direct lines of code were copied, just used for inspiration
'''
"Without freedom of choice there is no creativity."– James Kirk
'''

# Import libraries
import socket
import sys
import time

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


def numOfLoops(lengthVar):
    # find out how many chunks of 1000 you will send, ceiling it
    # https://www.geeksforgeeks.org/floor-ceil-function-python/
    loopsOfChunk1 = float(lengthVar) / 1000
    loopsOfChunkTrunk2 = int(loopsOfChunk1)
    print(loopsOfChunk1)
    print(loopsOfChunkTrunk2)

    #if original value and truncated value are not the same, we will increase truncated value by 1
    if loopsOfChunk1 != loopsOfChunkTrunk2:
        loopsOfChunk1 = loopsOfChunkTrunk2 + 1
        # this will be how many loops we will have to send
    print(f"Expecting {loopsOfChunk1} chunks")
    return loopsOfChunk1


# opens file and gets length
def openTextFile(userCommandArray1):
    textToChange = open(userCommandArray1)
    wholeFileToString1 = textToChange.read()
    textToChange.close()
    return wholeFileToString1



# -----
# Socket Port and IP 

SocketIP = returnIP()
print(SocketIP)

SocketPortNumber = returnPort()
print(SocketPortNumber)



#-------------------------------------
# Main Logic!
#-------------------------------------

jakeServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
jakeServerUDP.bind((SocketIP, SocketPortNumber))
jakeServerUDP.settimeout(None)

# --


# Variables
serverNeedToCensor = ''
serverSecretPhrase = ''


# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []
chunkBookmark = 0


serverNeedToCensorLength = 0
serverNeedToCensor = ''

# from Timeout
####
isTimeOut = 0
####


#-------------------------------------
# Main Logic!
#-------------------------------------


# shows server is up and running
print("Server Is Online")


# going to get data from client, loop until manually stoped
while True:
    # Server prints this if it has been successfully created
    print(f'The server is ready to receive on Hostname: {SocketIP}, Port: {SocketPortNumber}\n')

# ----
# # -----------
# # PUT COMMAND
# # -----------
# ----

    serverNeedToCensorLength, clientAddress = jakeServerUDP.recvfrom(2048)
    serverNeedToCensorLength = serverNeedToCensorLength.decode()
    print(f"LEN: {serverNeedToCensorLength}\n")


    # ack back
    recievedSuccessfully = "Length Recieved sucessfully!"
    jakeServerUDP.sendto(recievedSuccessfully.encode(), clientAddress)


    # finding number of loops
    loopsOfChunk = numOfLoops(serverNeedToCensorLength)

    # Going to recieve 
    currentChunkIndex = 0
    # Server Side File Storage
    ServerSideFileName = f"ServerNeedToCensor_UDP_{loopsOfChunk}"

    while (currentChunkIndex < int(loopsOfChunk)) and isTimeOut != 1:
        # Timeout after LEN: need to recieve data before one sec
        jakeServerUDP.settimeout(1)

        try:
            # Recieve incoming data before 1 sec
            serverNeedToCensor, clientAddress = jakeServerUDP.recvfrom(2048)
            inboundString = serverNeedToCensor.decode()

            # sending out ACK to client
            serverAckOutbound =  f"Chunk {currentChunkIndex} has been recieved!"
            jakeServerUDP.sendto(serverAckOutbound.encode(), clientAddress)
        except:
            print("Did not recieve data. Terminating")
            isTimeOut = 1 # will be used to skip other timeouts

        # Reset Timeout
        jakeServerUDP.settimeout(None)

        # Writing to file
        if currentChunkIndex == 0:

            # Creating File
            # Overwrite previous file with same name (so we don't accidentally append to it)
            with open(f"{ServerSideFileName}", 'w') as f:
                print(inboundString, end = '', file=f)

        else: 
            #Writing to file
            # https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
            with open(f"{ServerSideFileName}", 'a') as f:
                print(inboundString, end = '', file=f)

        # cleanup
        serverNeedToCensor = ''
        inboundString = ''
        currentChunkIndex += 1 

        # while loop ends ----
# --
        '''
        SENDING FIN MESSAGE
        NEED ACK MESSAGE BACK
        '''
        if (currentChunkIndex) == int(loopsOfChunk):
            serverFINMessage = "Server FIN Recieved!"
            
            # Sending Fin message to client
            jakeServerUDP.sendto(serverFINMessage.encode(), clientAddress)

            # Set timeout for 1 sec
            jakeServerUDP.settimeout(1)

            # recieving ack back
            try:
                serverNeedToCensor, clientAddress = jakeServerUDP.recvfrom(2048)
                serverNeedToCensor = serverNeedToCensor.decode()
                print(serverNeedToCensor)
            except:
                print("Data transmission terminated prematurely")
                isTimeOut = 1 # skips other timeouts if 1

            # reset timeout
            jakeServerUDP.settimeout(None)

# ----
# # ---------------
# # KEYWORD COMMAND
# # ---------------
# ----

    # TEST isTimeOut flag to see if sections will skip if it is not false
    if isTimeOut != 1:
        # Accepting the word to censor from client
        # AND target file's filename from client
        serverKeywordData, clientAddress = jakeServerUDP.recvfrom(2048)
        serverKeywordArray = (serverKeywordData.decode()).split(' ', 1)


    # Timeout - ACK
    # --
        # # send response back to client
        # # Sending back name of the new censored file
        # # make this a normal ack
        serverAckOutbound =  f"Keyword: {serverKeywordArray[0]} has been recieved!"
        jakeServerUDP.sendto(serverAckOutbound.encode(), clientAddress)
        print(serverAckOutbound)

        print("Waiting for ACK Confirmation\n")
        '''
        SERVER TIMEOUT - Recieving Confirmation of ACK recipt on server
        '''
        jakeServerUDP.settimeout(1)
        try:
        #     # # # getting response back
            serverConfirmation2, clientAddress = jakeServerUDP.recvfrom(2048)
            serverConfirmation2 = serverConfirmation2.decode()
            print(f"Response from Client: {serverConfirmation2}\n")
        except:
            print("Response not recieved for keyword ACK. Terminating.")
            isTimeOut = 1 # will be used to skip other timeouts
        
        jakeServerUDP.settimeout(None)


    # ---
    # do if statement 
        if isTimeOut != 1:
            # Getting Phase to Censor
            serverSecretPhrase = serverKeywordArray[0]
            print(f"Top Secret Word to censor is: {serverSecretPhrase}")

            # creating string to replace target phrase with
            serverReplacementString = myFindTargetString(serverSecretPhrase)
            print(f"Replacement String will be: {serverReplacementString}")

            # opening new anon file
            # https://docs.python.org/3/library/functions.html#open
            textToChange = open(f"{ServerSideFileName}")
            serverWholeFileToString = textToChange.read()
            textToChange.close()
        
            # New Filenames
            newCensoredFileName = f"Anon_{serverKeywordArray[1]}"

# # --------------------------##
#    Anonymize happens here    #
# # --------------------------##

            # Doing find and replace
            # from https://www.geeksforgeeks.org/python-string-replace/
            serverCensoredOutput = serverWholeFileToString.replace(serverSecretPhrase, serverReplacementString)
        
            # Overwriting any previous file with the same name
            f = open(f"server_{newCensoredFileName}", "w")

            # Output sting to file
            # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
        
            with open(f"server_{newCensoredFileName}", 'a') as f:
                print(serverCensoredOutput, end = '', file=f)


# Sending Confirmation of Scrambling + new name of the file to client
        
            messageRecieved = f"File {serverKeywordArray[1]} has been anonymized. Output file is: {newCensoredFileName}"
            print(messageRecieved)

            jakeServerUDP.sendto(messageRecieved.encode(), clientAddress)
            '''
            TIMEOUT NEEDED FOR ACK
            '''
            # will need to send ack confirmation as well

            # Timeout for 1 sec
            jakeServerUDP.settimeout(1)

            try: 
                # receiving client ACK
                serverConfirmation2, clientAddress = jakeServerUDP.recvfrom(2048)
                serverConfirmation2 = serverConfirmation2.decode()
                print(f"Response from Client: {serverConfirmation2}\n")

                # sending out ACK for client ACK
                serverAckOutbound =  f"New Anon Message: Client ACK has been recieved!"
                jakeServerUDP.sendto(serverAckOutbound.encode(), clientAddress)
            except:
                print("Response not recieved ACK for Anon Name Message. Terminating.")
                isTimeOut = 1 # will be used to skip other timeouts

            # reset timeout
            jakeServerUDP.settimeout(None)
        
        else:
            print("Skipped Scrambling due to timeout!")

# ----
# # -----------
# # GET COMMAND
# # -----------
# ----

    # if timeout check
    if isTimeOut != 1:
        # Recieving Get request from user
        serverGetRequest, clientAddress = jakeServerUDP.recvfrom(2048)
        serverGetRequest = serverGetRequest.decode("utf-8")
        print(f"Get Request Recieved: {serverGetRequest}")

        '''
        SEND ACK TO CLIENT
        '''
        # sending out ACK for client get
        serverAckOutbound =  f"Client Get request has been recieved for: {serverGetRequest}!"
        jakeServerUDP.sendto(serverAckOutbound.encode(), clientAddress)

        '''
        TIMEOUT - NEED ACK BACK
        '''

        jakeServerUDP.settimeout(1)

        try: 
            # receiving client ACK
            serverConfirmation2, clientAddress = jakeServerUDP.recvfrom(2048)
            serverConfirmation2 = serverConfirmation2.decode()
            print(f"Response from Client: {serverConfirmation2}\n")

        except:
            print("Data Transmission Terminated prematurely.")
            isTimeOut = 1 # will be used to skip other timeouts

        # reset timeout
        jakeServerUDP.settimeout(None)


    # if timeout check
    if isTimeOut != 1:

        # Sending length
        # opening file
        serverGetRequest = f"server_{serverGetRequest}"
        print(serverGetRequest)
        wholeFileToString = openTextFile(serverGetRequest)

        # Get length
        wholeFileToStringLength = str(len(wholeFileToString))


        # transmitting length to client 
        jakeServerUDP.sendto(wholeFileToStringLength.encode(), clientAddress)
        '''
        TIMEOUT - NEED ACK BACK
        '''
        jakeServerUDP.settimeout(1)

        try: 
            # receiving client ACK
            serverConfirmation2, clientAddress = jakeServerUDP.recvfrom(2048)
            serverConfirmation2 = serverConfirmation2.decode()
            print(f"Response from Client: {serverConfirmation2}\n")

            # sending out ACK for client ACK
            serverAckOutbound =  f"Length: Client ACK has been recieved!"
            jakeServerUDP.sendto(serverAckOutbound.encode(), clientAddress)
        except:
            print("Did not recieve ACK. Terminating.")
            isTimeOut = 1 # will be used to skip other timeouts

        # reset timeout
        jakeServerUDP.settimeout(None)

# --
    # sending chunks to client
    # if timeout check
    if isTimeOut != 1:
        
        outboundChunk = ''
        chunks = 0
        starterPoint = 0

        # WHILE LOOP HERE
        while chunks <= loopsOfChunk and isTimeOut != 1:
            endPoint = starterPoint + 1000
            
            # chunking data
            outboundChunk = wholeFileToString[starterPoint:endPoint]

            # Sending Data to client
            jakeServerUDP.sendto(outboundChunk.encode("utf-8"), clientAddress)
            '''
            File recieved ACK - Incoming
            '''
            # timeout for 1 sec
            jakeServerUDP.settimeout(1)

            try:
                ifAcked, clientAddress = jakeServerUDP.recvfrom(2048)
                ifAcked = ifAcked.decode()
                print(f"{chunks} From Server: {ifAcked}")
            except:
                # timeout error for no confirmation of data
                print("Did not recieve ACK. Terminating. (File Upload)")
                isTimeOut = 1
            # reset timeout
            jakeServerUDP.settimeout(None) 

            #cleanup
            ifAcked = ''
            outboundChunk = ''
            starterPoint = endPoint
            chunks += 1
    # ----
        '''
        RECIEVING FIN MESSAGE
        SEND ACK MESSAGE BACK
        '''
        # set timeout to 1 sec

        confirmationServer2 = 'Confirmation Recipt - FIN message'
        jakeServerUDP.settimeout(1)
        
        try:
            ifAcked, clientAddress = jakeServerUDP.recvfrom(2048)
            ifAcked = ifAcked.decode()
            print(ifAcked)
            
            #sending fin recipt back
            jakeServerUDP.sendto(confirmationServer2.encode("utf-8"), (SocketIP, SocketPortNumber))

            # Recieving FIN
            ifAcked, clientAddress = jakeServerUDP.recvfrom(2048)
            ifAcked = ifAcked.decode()
            print(ifAcked)
            
        except:
            # timeout error for no confirmation of data
            print("Did not recieve ACK. Terminating. (File Upload)")
            isTimeOut = 1

        
        # reset timout 
        jakeServerUDP.settimeout(None)

        #cleanup
        ifAcked = ''
    
    else:
        print("Timeout Triggered")


# ---
    print("\n\nProcess Completed!\n\n")
    # reset isTimeout
    isTimeOut = 0
# ---

