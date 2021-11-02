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






# -----
# Socket Port and IP 

SocketIP = returnIP()
print(SocketIP)

SocketPortNumber = returnPort()
print(SocketPortNumber)



# Main Logic
# ---

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


# ---
# Program logic
# ---


# shows server is up and running
print("Server Is Online")


# going to get data from client, loop until manually stoped
while True:
    # Server prints this if it has been successfully created
    print(f'The server is ready to receive on Hostname: {SocketIP}, Port: {SocketPortNumber}')

    #     # -----------
    #     # PUT COMMAND
    #     # -----------

    serverNeedToCensorLength, clientAddress = jakeServerUDP.recvfrom(2048)
    serverNeedToCensorLength = serverNeedToCensorLength.decode()
    print(f"LEN: {serverNeedToCensorLength}")

    # test sleep
    #time.sleep(2)

    # ack back
    recievedSuccessfully = "Length Recieved sucessfully!"
    jakeServerUDP.sendto(recievedSuccessfully.encode(), clientAddress)

    # finding number of loops
    loopsOfChunk = numOfLoops(serverNeedToCensorLength)


    # while loop starts ----
    # Timeout after LEN: need to recieve data before one sec
    jakeServerUDP.settimeout(1)

    try:
        # Recieve incoming data before 1 sec
        serverNeedToCensor, clientAddress = jakeServerUDP.recvfrom(2048)
        serverNeedToCensor = serverNeedToCensor.decode()
        print(serverNeedToCensor)

        # sending out ACK to client
        recievedSuccessfully = "File Recieved sucessfully!"
        jakeServerUDP.sendto(recievedSuccessfully.encode(), clientAddress)
    except:
        print("Did not recieve data. Terminating")
        isTimeOut = 1 # will be used to skip other timeouts

    # Reset Timeout
    jakeServerUDP.settimeout(None)
    # while loop ends ----


    # TEST isTimeOut flag to see if sections will skip if it is not false

    if isTimeOut == 0:
        print(f"Num of Loops: {loopsOfChunk}")


# ---

    # reset isTimeout
    isTimeOut = 0


# ---

# ---
# recieving incoming chunks:

#     # Creating String to write recive from 
#     serverNeedToCensor = ''

#     # Going to recieve 
#     currentChunkIndex = 0
    

#     # Server Side File Storage
#     ServerSideFileName = f"{serverOriginalFileName}_"


#     while currentChunkIndex < int(serverLoopsOfChunk):
#         print(f"On String Section Section {currentChunkIndex}")
#         print(f"Need to get to {int(serverLoopsOfChunk)}")

#         # Recieving string in byte incriments
#         serverNeedToCensor  = clientSocket.recv(65000)
#         inboundString = serverNeedToCensor.decode("utf-8")
#         print(inboundString)

#         # creating ACK
#         serverAckOutbound =  f"Chunk {currentChunkIndex} has been recieved!"


#         if currentChunkIndex == 0:

#             # Creating File
#             # Overwrite previous file with same name (so we don't accidentally append to it)
#             with open(f"{serverOriginalFileName}_", 'w') as f:
#                 print(inboundString, end = '', file=f)

#             print("1st statement")
#             # cleanup
#             inboundString = ''
#             currentChunkIndex += 1 

#             # Sending Ack
#             clientSocket.send(serverAckOutbound.encode())    
            
#         else:

#             #Writing to file
#         # https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
#             with open(f"{serverOriginalFileName}_", 'a') as f:
#                 print(inboundString, end = '', file=f)
        
#             print("2nd Statement")
#             # incriment
#             currentChunkIndex += 1 

#             # cleanup
#             inboundString = ''

#             # Sending Ack
#             clientSocket.send(serverAckOutbound.encode())

#      # Sending ACK
#     clientSocket.send(serverAckOutbound.encode())

#     print("Done with Recieving!")


# # ---