# Import libraries
import socket
import sys
import time

# ---

# Functions:

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


def openTextFile(userCommandArray1):
    filePath = userCommandArray1[1]
    textToChange = open(filePath)
    wholeFileToString1 = textToChange.read()
    textToChange.close()
    return wholeFileToString1



# -----
# Socket Port and IP 

SocketIP = returnIP()
print(SocketIP)

SocketPortNumber = returnPort()
print(SocketPortNumber)

#Setting up socket 
jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ---

# Variables
userCommand = ''
userCommandArray = ['', '']
confirmationServerAck = ''

####
isTimeOut = 0
####




#-------------------------------------
# Main Logic!
#-------------------------------------

# ----
# # -----------
# # PUT COMMAND
# # -----------
# ----
userCommand = input("Enter Command: ")

# Split on String
# https://www.tutorialspoint.com/python/string_split.htm
userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")


# Getting file length
wholeFileToString = openTextFile(userCommandArray)

# Get length
wholeFileToStringLength = str(len(wholeFileToString))
print(wholeFileToStringLength)

# finding number of loops
loopsOfChunk = numOfLoops(len(wholeFileToString))


#LENGTH SEND - NEED ACK OUT AND ACK BACK
# Sending length of file to server first
jakeClientUDP.sendto(wholeFileToStringLength.encode(), (SocketIP, SocketPortNumber))
'''
Length Ack - Incoming
'''
# timeout for 1 sec
jakeClientUDP.settimeout(1)

try:
    # Recieving server ack
    ifAcked, clientAddress = jakeClientUDP.recvfrom(2048)
    ifAcked = ifAcked.decode()
    print(f"From Server: {ifAcked}")
except:
    # timeout error for no length ack
    print("Did not recieve ACK. Terminating. (Length)")
    isTimeOut = 1
#reset timeout
jakeClientUDP.settimeout(None) 

#cleanup
ifAcked = ''


# if timeout check
if isTimeOut != 1:
    
    outboundChunk = ''
    chunks = 0
    starterPoint = 0

    # WHILE LOOP HERE
    while chunks < loopsOfChunk and isTimeOut != 1:
        endPoint = starterPoint + 1000
        
        # chunking data
        outboundChunk = wholeFileToString[starterPoint:endPoint]

        # Sending Data to Server
        jakeClientUDP.sendto(outboundChunk.encode("utf-8"), (SocketIP, SocketPortNumber))
        '''
        File recieved ACK - Incoming
        '''
        # timeout for 1 sec
        jakeClientUDP.settimeout(1)

        try:
            ifAcked, clientAddress = jakeClientUDP.recvfrom(2048)
            ifAcked = ifAcked.decode()
            print(f"{chunks} From Server: {ifAcked}")
        except:
            # timeout error for no confirmation of data
            print("Did not recieve ACK. Terminating. (File Upload)")
            isTimeOut = 1
        # reset timeout
        jakeClientUDP.settimeout(None) 

        #cleanup
        ifAcked = ''
        outboundChunk = ''
        starterPoint = endPoint
        chunks += 1
else:
    print("Timeout Triggered")


# ----
# # ---------------
# # KEYWORD COMMAND
# # ---------------
# ----
# if timeout check
if isTimeOut != 1:
    # checking to see if quit
    if userCommandArray[0].lower() != 'quit':
        userCommand = input("Enter command: ")
        # Split on String
        # https://www.tutorialspoint.com/python/string_split.htm
        userCommandArray = userCommand.split(' ', 1)
        print(f"User command: {userCommandArray[0]}")


    # quit condition (from keyword command input)
    if userCommandArray[0].lower() == 'keyword':
        # specifies phrase to censor & file to have server censor it on
        # sends it to server
        jakeClientUDP.sendto(str(userCommandArray[1]).encode("utf-8"), (SocketIP, SocketPortNumber))
        # Waiting for Server Response
        print("Keyword: Awaiting server response.")
        '''
        TIMEOUT - WAITING FOR ACK BACK
        '''
        jakeClientUDP.settimeout(1)

        try:
            # Recieving confirmation back from server
            confirmationServer1, clientAddress = jakeClientUDP.recvfrom(2048)
            print(confirmationServer1.decode("utf-8"))

        except:
            print("Did not get Keyword Ack Back. Terminating")
            isTimeOut = 1

        # reset timeout
        jakeClientUDP.settimeout(None) 
# ---
                
        '''
        SERVER TIMEOUT - Sending Confirmation of Ack recipt back to server
        '''
        confirmationServer2 = 'Server Ack Recieved'
        jakeClientUDP.sendto((confirmationServer2).encode("utf-8"), (SocketIP, SocketPortNumber)) 

else:
    print("Timeout Triggered 2")

if isTimeOut != 1:
    print("If you see this, we moved onto the next phase")


# #CONVERT FROM TCP
# # Data sending to server
# # ----
#     # Chunk String, Send Out
#     # ----
#     outboundChunk = ''

#     chunks = 0
#     starterPoint = 0
#     while chunks < loopsOfChunk:

#         endPoint = starterPoint + 1000

#         # Sending
#         jakeClient.send(wholeFileToString[starterPoint:endPoint].encode())


#         print(f"On chunk: {chunks}, String to append is: {wholeFileToString[starterPoint:endPoint]}")

#         starterPoint = endPoint
#         chunks += 1


#         # # wait for ACK

#         print("Waiting for ACK")

#         # # Recieving ACK from Server
#         ifAcked, clientAddress = jakeClient.recvfrom(2048)
#         ifAcked = ifAcked.decode("utf-8")

#         print(f"Server Says: {ifAcked}")


#         # # clean up
#         ifAcked = ''




# closeout
jakeClientUDP.close()