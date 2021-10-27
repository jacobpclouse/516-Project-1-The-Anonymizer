''' 

STOP N WAIT
Inspired by the UDP section in the textbook - 2.7

'''

import socket
import sys
import time

# Socket Functions:

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

# ---

# Server prints this if it has been successfully created
print('The server is ready to receive')

while True:
    # Recieving uncensored text string from client
    uncensoredText, clientAddress = jakeServerUDP.recvfrom(65000)

    # Putting uncensored text into modified variable
    serverNeedToCensor = uncensoredText.decode()

    # Wait X seconds
    #time.sleep(5)

    # Server Ack message sent to client - Text
    ackToClient = "Text Recieved on Server"
    jakeServerUDP.sendto(ackToClient.encode(), clientAddress)
# --

    # Recieving Top Secret phrase from client
    topSecretPhrase, clientAddress = jakeServerUDP.recvfrom(2048)

    # Putting Top Secret phrase into modified variable
    serverSecretPhrase = topSecretPhrase.decode()

    # Wait X seconds
    #time.sleep(5)

    # Server Ack message sent to client - Keyword
    ackToClient = "Keyword Recieved on Server"
    jakeServerUDP.sendto(ackToClient.encode(), clientAddress)

# --

    # Recieving replacement character from client
    replacementChar, clientAddress = jakeServerUDP.recvfrom(2048)

    # Putting replacement character into modified variable
    serverReplacementChar = replacementChar.decode()

    # Wait X seconds
    #time.sleep(5)

    # Server Ack message sent to client - Replacement Char
    ackToClient = "Replacement Char Recieved on Server"
    jakeServerUDP.sendto(ackToClient.encode(), clientAddress)

# --

    # Discovering the length of the Top secret phrase length
    # from https://www.geeksforgeeks.org/python-string-length-len/
    lengthOfCensorPhrase = len(serverNeedToCensor)
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

    # Send back to user
    #time.sleep(11)
    jakeServerUDP.sendto(censoredOutput.encode(), clientAddress)
