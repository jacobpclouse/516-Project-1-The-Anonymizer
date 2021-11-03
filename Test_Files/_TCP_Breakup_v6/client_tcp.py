# THIS USES PYTHON Python 3.8.10
# This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
# No direct lines of code were copied, just used for inspiration
"""
"Logic is the beginning of wisdom, not the end." – Spock
"""


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

# ---

# Taking the values for IP and Port from command line arguments
SocketIP = returnIP()
print(SocketIP)
SocketPortNumber = returnPort()
print(SocketPortNumber)

# Creating & Binding Server to Specified IP & Port

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeClient.connect((SocketIP, SocketPortNumber))

# ---

# Variables
userCommand = ''
userCommandArray = ['', '']

lengthOfChunk = 1000
# ---

# -----------------------------------
# Main Logic!
# -----------------------------------


# -----------
# PUT COMMAND
# -----------

# while userCommandArray[0].lower() != 'quit':
userCommand = input("Enter Command: ")

# Split on String
# https://www.tutorialspoint.com/python/string_split.htm
userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")

# quit condition
if userCommandArray[0].lower()  == 'put':
    # opening file
    # https://docs.python.org/3/library/functions.html#open
    filePath = userCommandArray[1]
    textToChange = open(filePath)
    wholeFileToString = textToChange.read()
    textToChange.close()

    # Store Length to a variable
    fileLengthVar = len(wholeFileToString)
    #print(f"The length of the file is: {fileLengthVar}")

    # # sending original filename to server
    jakeClient.send(filePath.encode())

# ---

    # -----------
    # Need To Send Length to server
    # -----------


    # find out how many chunks of 4000 you will send, ceiling it
    # https://www.geeksforgeeks.org/floor-ceil-function-python/
    loopsOfChunk = fileLengthVar / lengthOfChunk
    loopsOfChunkTrunk = int(loopsOfChunk)

    #if original value and truncated value are not the same, we will increase truncated value by 1
    if loopsOfChunk != loopsOfChunkTrunk:
        loopsOfChunk = loopsOfChunkTrunk + 1

    # converting to string for ease
    outboundLoops = str(loopsOfChunk)

    # Sending number of chunks to server first
    jakeClient.send(outboundLoops.encode())

    # Recieving ACK
    clientAck, clientAddress = jakeClient.recvfrom(2048)
    #print(f"Server Length Response: {clientAck}")

    # ----
    # Chunk String, Send Out
    # ----
    outboundChunk = ''

    chunks = 0
    starterPoint = 0
    while chunks < loopsOfChunk:

        endPoint = starterPoint + lengthOfChunk

        # Sending string (1000 chunks at a time)
        jakeClient.send(wholeFileToString[starterPoint:endPoint].encode())

        #print(f"On chunk: {chunks}, String to append is: {wholeFileToString[starterPoint:endPoint]}")
        starterPoint = endPoint
        chunks += 1

        # # Recieving ACK from Server
        ifAcked, clientAddress = jakeClient.recvfrom(2048)
        ifAcked = ifAcked.decode("utf-8")

        # # clean up
        ifAcked = ''

    # cleaning up
    userCommand = ''
    confirmationServer1 = ''


# ----
# ---------------
# KEYWORD COMMAND
# ---------------
# ----
    # prompting user for next command
    userCommand = input("Enter command: ")
    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    userCommandArray = userCommand.split(' ', 1)
    #print(f"User command: {userCommandArray[0]}")


# also checking to see if quit command is not active
if userCommandArray[0].lower()  == 'keyword':
    
    # # specifies phrase to censor & file to have server censor it on
    # sends it to server
    userCensorPhrase = userCommandArray[1]
    jakeClient.send(userCensorPhrase.encode())

    # Waiting for Server Response
    print("KEYWORD Awaiting server response.")

    # Recieving confirmation back from server
    confirmationServer1 = jakeClient.recv(2048).decode("utf-8")
    print(confirmationServer1)


    # cleaning up
    userCommand = ''
    userCommandArray = ['', '']
    confirmationServer1 = ''

# ----
# -----------
# GET COMMAND
# -----------
# ----
    # prompting user for next command
    userCommand = input("Enter command: ")
#     # Split on String
#     # https://www.tutorialspoint.com/python/string_split.htm
    userCommandArray = userCommand.split(' ', 1)
    #print(f"User command: {userCommandArray[0]}")


if userCommandArray[0].lower() == 'get':
    
    #print(userCommandArray[1])
    userGetRequest = userCommandArray[1]

    # sending Get command and request for filename to server
    jakeClient.send(userGetRequest.encode())
#---

    # use same number of loops as above as it should be the same
    # Creating String to write recive from 
    censoredMessage = ''

    # Going to recieve 
    currentChunkIndex = 0

    # client Side Filename
    censoredTextFileName = f"TCP_Anon{filePath}"


    while currentChunkIndex < int(loopsOfChunk):
        # Recieving string in byte incriments
        censoredMessage = jakeClient.recv(65000)
        censoredMessage = censoredMessage.decode("utf-8")

        # creating ACK
        serverAckOutbound =  f"Chunk {currentChunkIndex} has been recieved!"

        if currentChunkIndex == 0:

            # Creating File (Overwriting if exits already)
            # https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
            with open(f"{censoredTextFileName}", 'w') as f:
                print(censoredMessage, end = '', file=f)

            # incriment
            currentChunkIndex += 1 

            # cleanup
            censoredMessage = ''

            # Sending Ack
            jakeClient.send(serverAckOutbound.encode())


        else:

            #Writing to file
            # https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
            with open(f"{censoredTextFileName}", 'a') as f:
                print(censoredMessage, end = '', file=f)
        
            #print("2nd Statement")
            # incriment
            currentChunkIndex += 1 

            # cleanup
            censoredMessage = ''

            # Sending Ack
            jakeClient.send(serverAckOutbound.encode())


     # Sending ACK
    jakeClient.send(serverAckOutbound.encode())

    print("\nDone with Recieving!")
    print(f"\nFile saved locally as: TCP_{userCommandArray[1]}")


# ----
# -----------
# QUIT COMMAND
# -----------
# ----
    userCommand = input("Enter command: ")
    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    userCommandArray = userCommand.split(' ', 1)
    print(f"User command: {userCommandArray[0]}")

if userCommandArray[0].lower() == 'quit':
    
    print("Quitting...")
    jakeClient.close()



# closing out
jakeClient.close()
