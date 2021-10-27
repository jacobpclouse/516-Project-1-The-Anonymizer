''' 

STOP N WAIT
Inspired by the UDP section in the textbook - 2.7

Could I possibly just append the top secret phrase and secret character to the end of the 
full string and then remove them later? Get length of string before and after and add that as well?

2) how can we set is so that the server knows to move along?
'''

import socket
import sys

# Socket Variables:

def returnIP():
    incomingIP = sys.argv[1]
    return incomingIP


def returnPort():
    incomingPort = int(sys.argv[2])
    return incomingPort

# -----
# Socket Port and IP 

SocketIP = returnIP()
print(SocketIP)
SocketPortNumber = returnPort()
print(SocketPortNumber)


# ---

jakeServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
jakeServerUDP.bind((SocketIP, SocketPortNumber))

# --

# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []
chunkBookmark = 0

# Functions:


def chunkerFunction(string):

    # Function Variables:

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

    # ---

    # Function Logic:

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


# ---

# Server prints this if it has been successfully created
print('The server is ready to receive')

while True:
    # Recieving uncensored text string from client
    uncensoredText, clientAddress = jakeServerUDP.recvfrom(2048)

    # Putting uncensored text into modified variable
    serverNeedToCensor = uncensoredText.decode()

# --

    # Recieving Top Secret phrase from client
    topSecretPhrase, clientAddress = jakeServerUDP.recvfrom(2048)

    # Putting Top Secret phrase into modified variable
    serverSecretPhrase = topSecretPhrase.decode()

# --

    # Recieving replacement character from client
    replacementChar, clientAddress = jakeServerUDP.recvfrom(2048)

    # Putting replacement character into modified variable
    serverReplacementChar = replacementChar.decode()

# --

    # Discovering the length of the Top secret phrase length
    # from https://www.geeksforgeeks.org/python-string-length-len/
    lengthOfCensorPhrase = len(serverNeedToCensor)
    print(
        f"RECIEVED {serverNeedToCensor, serverSecretPhrase, serverReplacementChar} FROM {clientAddress}")
    print(
        f"The Top secret phrase: {serverSecretPhrase} has {lengthOfCensorPhrase} characters")
# --

    # Gets length of string and creates the character to replace it with
    replacementString = ''

    for letters in serverSecretPhrase:
        replacementString += serverReplacementChar

    print(f"The Replacement string will be {replacementString}")

# --

    # Doing find and replace
    # from https://www.geeksforgeeks.org/python-string-replace/
    censoredOutput = serverNeedToCensor.replace(
        serverSecretPhrase, replacementString)
    # print(censoredOutput)

    # Send back to user
    jakeServerUDP.sendto(censoredOutput.encode(), clientAddress)
