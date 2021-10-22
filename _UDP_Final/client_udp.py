''' 

STOP N WAIT
Inspired by the UDP section in the textbook - 2.7

'''

# put uncensored_text.txt

# Import libraries
import socket
import sys


# Variables: 

# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []
chunkBookmark = 0
userCommand = ''

# --


# Functions:


# importing Command line arguments - for port number
# https://cs.stanford.edu/people/nick/py/python-main.html

def returnPort():
    inputVar = int(sys.argv[1])
    return inputVar
    # Return Statement in function to return value
    # https://www.w3schools.com/python/python_functions.asp



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

# Setting Up UDP Connection with SOCK_DGRAM
jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Grabbing Hostname and Port
SocketIP = socket.gethostname()
SocketPortNumber = returnPort()


# ---

# Main Logic!
    # try breaking this out into its own function if it works (then can call it)
    # ** Might try having the entire function under this command if it works (empty string)
while userCommand == '':
    userCommand = input("Waiting for Put command: ")

    if userCommand.lower() == 'quit':
        break

    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    # ** break out into function
userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")



# 'put' Command
# opening file

filePath = userCommandArray[1]
textToChange = open(filePath)
wholeFileToString = textToChange.read()
textToChange.close()


print(wholeFileToString)

        # ----

# Getting length of string and sending it to server
#lenString = str(len(wholeFileToString))
#jakeClientUDP.sendto(lenString.encode(), (SocketIP, SocketPortNumber))

        # ----
# sending put string to server
# assuming first string is always 'put'
jakeClientUDP.sendto(wholeFileToString.encode(), (SocketIP, SocketPortNumber))

# sending put filepath
jakeClientUDP.sendto(filePath.encode(), (SocketIP, SocketPortNumber))

userCommand = ''
userCommandArray = []

# ---

    # keyword
    # prompting user for next command
while userCommand == '':
    userCommand = input("Waiting for Keyword command: ")

    if userCommand.lower() == 'quit':
        break

    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    # Split twice for keyword
userCommandArray = userCommand.split(' ', 2)
print(f"User command: {userCommandArray[0]}")


# -- 

# 'keyword' command
# specifies phrase to censor AND file to censor the word in
userCensorPhraseNFile = userCommandArray[1]
userCensorKeywordFilePath = userCommandArray[2]
print(userCensorPhraseNFile)

# sending keyword phrase and filename to operate on to server
# assuming second string is always 'keyword'
jakeClientUDP.sendto(userCensorPhraseNFile.encode(), (SocketIP, SocketPortNumber))


# sending keyword path, will compare on serverside that this is right
jakeClientUDP.sendto(userCensorKeywordFilePath.encode(), (SocketIP, SocketPortNumber))

userCommandArray = []
userCommand = ''

# --

    # Get command
    # prompting user for next command
while userCommand == '':
    userCommand = input("Waiting for Get command: ")

    if userCommand.lower() == 'quit':
        break

    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    # ** break out into function
userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")

# -- determining what filename will be
userGetRequest = userCommandArray[0]
userGetRequestFilePath = userCommandArray[1]


# sending Get command and request for filename to server
# assuming third string is always 'get'
jakeClientUDP.sendto(userGetRequest.encode(), (SocketIP, SocketPortNumber))

# --

#Getting censored message back from server & printing out
censoredMessage, serverAddress = jakeClientUDP.recvfrom(2048)
print(f'From Server: {censoredMessage.decode()}')


#---

# printing to standard out
# from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
with open(f'./OutputText/{userGetRequestFilePath}.txt', 'w') as f:
    print(censoredMessage, file=f)


print(censoredMessage.decode())
jakeClientUDP.close()









# # Imports data from file into a string
# # from https://www.tutorialkart.com/python/python-read-file-as-string/
# textToChange = open(pathName)
# wholeFileToString = textToChange.read()
# textToChange.close()
# print(wholeFileToString)


# # Finding Out what the censored phrase is from user & phrase length
# # from https://www.geeksforgeeks.org/python-string-length-len/
# censorPhrase = input("What phrase is classified: ")
# #lengthOfCensorPhrase = len(censorPhrase)

# # Finding out what the replacement character is
# replaceChar = input("What do you want to replace it with: ")


# # Sending text to server so it can be censored
# # Can I send multiple strings to the server? Will it accept them?
# jakeClientUDP.sendto(wholeFileToString.encode(), (SocketIP, SocketPortNumber))


# jakeClientUDP.sendto(censorPhrase.encode(), (SocketIP, SocketPortNumber))


# jakeClientUDP.sendto(replaceChar.encode(), (SocketIP, SocketPortNumber))


# # Recieving censored text back & saving to file
# censoredMessage, serverAddress = jakeClientUDP.recvfrom(2048)

# # printing to standard out
# # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
# with open('./UDP_Censored_Output/TopSecretUDP.txt', 'w') as f:
#     print(censoredMessage, file=f)


# print(censoredMessage.decode())


# jakeClientUDP.close()

# # ---
