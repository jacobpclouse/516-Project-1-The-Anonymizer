''' 

STOP N WAIT
Inspired by the UDP section in the textbook - 2.7

/media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/Test_Files/UncensoredText/uncensored.txt
'''

import socket
import sys


jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ---
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

def returnIP():
    incomingIP = sys.argv[1]
    return incomingIP


def returnPort():
    incomingPort = int(sys.argv[2])
    return incomingPort


# ---

# Normal Variables:

SocketIP = socket.gethostname()
SocketPortNumber = 12001


# ---

# Getting File Path Location
pathName = input("List the path name for the import file WITHOUT QUOTES: ")
print(pathName)


# Imports data from file into a string
# from https://www.tutorialkart.com/python/python-read-file-as-string/
textToChange = open(pathName)
wholeFileToString = textToChange.read()
textToChange.close()
print(wholeFileToString)


# Finding Out what the censored phrase is from user & phrase length
# from https://www.geeksforgeeks.org/python-string-length-len/
censorPhrase = input("What phrase is classified: ")
#lengthOfCensorPhrase = len(censorPhrase)

# Finding out what the replacement character is
replaceChar = input("What do you want to replace it with: ")


# Sending text to server so it can be censored
# Can I send multiple strings to the server? Will it accept them?
jakeClientUDP.sendto(wholeFileToString.encode(), (SocketIP, SocketPortNumber))


jakeClientUDP.sendto(censorPhrase.encode(), (SocketIP, SocketPortNumber))


jakeClientUDP.sendto(replaceChar.encode(), (SocketIP, SocketPortNumber))


# Recieving censored text back & saving to file
censoredMessage, serverAddress = jakeClientUDP.recvfrom(2048)

# printing to standard out
# from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
with open('./UDP_Censored_Output/TopSecretUDP.txt', 'w') as f:
    print(censoredMessage, file=f)


print(censoredMessage.decode())


jakeClientUDP.close()

# ---
