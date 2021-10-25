# THIS USES PYTHON Python 3.8.10

"""
You can re-run the client to re-execute the program
Send data as soon as you get it (ie: get a put, then send it off right away, don't wait and lump together)

You don't need to keep track of state for TCP
You can assume that the file will be in the same directory as the program
You can use main function and pass in port number as an argument
You can assume that put comes first, then keyword, then get (can throw an error if empty)
KEYWORD command only gives you the keyword to censor and points to the filename to censor it on
ACK command will be impliment like you previously tried to impliment PUT command (ie: with STATE)
Don't overwrite your files! put them in seperate directories!
Don't worry about sequence numbers and duplicates for your UDP implimentation
You can have x2 receivers on the server side, just needs program to repeat!
If the user makes a mistake (ie: gives wrong keyword) that on them (don't worry about giving them another shot)

** THINK about HOW you are going to impliment string splitting!
"""

# put File4.txt
# keyword ICSI File4.txt
# get AnonFile4.txt

# keyword 516 File4.txt

# -----------------------------------
# -----------------------------------

# Import libraries
import socket
import sys

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


def chunkerFunction(string):
    #-------------------
    # chunker Variables: 
    #-------------------

    # getting length of string
    stringLength = len(string)
    print(f"Length of String: {stringLength} characters")

    # determining the target size (ie: this will be 1000 for udp)
    byteSize = 1000

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
print(SocketIP)
SocketPortNumber = returnPort()
print(SocketPortNumber)

#jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
#jakeClient.connect((SocketIP, SocketPortNumber))
jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ---

# Variables
userCommand = ''
userCommandArray = ['', '']


# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []
chunkBookmark = 0

# ---

# Main Logic!


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
if userCommandArray[0].lower() != 'quit':
    # opening file
    # https://docs.python.org/3/library/functions.html#open
    filePath = userCommandArray[1]
    textToChange = open(filePath)
    wholeFileToString = textToChange.read()
    textToChange.close()

    print(f"The length of the file is: {len(wholeFileToString)}")

    # -----------
    # Need To Send Length to server
    # -----------



    # sending original filename to server
    #jakeClient.send(filePath.encode())
    jakeClientUDP.sendto(filePath.encode(), (SocketIP, SocketPortNumber))

    # sending put string to server
    # assuming first string is always 'put'
    jakeClient.send(wholeFileToString.encode())
    print("Awaiting Server Response")

    # Recieving confirmation back from server
    confirmationServer1 = jakeClient.recv(2048).decode("utf-8")
    print(confirmationServer1)

    # cleaning up
    userCommand = ''
    confirmationServer1 = ''
else:
    print('Quit Statement Active 1')
    jakeClient.close()

# # ---



# ---------------
# KEYWORD COMMAND
# ---------------

# prompting user for next command
# also checking to see if quit command is not active
if userCommandArray[0].lower() != 'quit':
    userCommand = input("Enter command: ")

#     # Split on String
#     # https://www.tutorialspoint.com/python/string_split.htm
    userCommandArray = userCommand.split(' ', 1)
    print(f"User command: {userCommandArray[0]}")

# quit condition
if userCommandArray[0].lower() != 'quit':
    print(userCommandArray[1])


    # # --

    # # specifies phrase to censor & file to have server censor it on
    # sends it to server
    userCensorPhrase = userCommandArray[1]
    jakeClient.send(userCensorPhrase.encode())

    # Waiting for Server Response
    print("Awaiting server response.")

    # Recieving confirmation back from server
    confirmationServer1 = jakeClient.recv(2048).decode("utf-8")
    print(confirmationServer1)

    # cleaning up
    userCommand = ''
    userCommandArray = ['', '']
    confirmationServer1 = ''
else:
    print('Quit Statement Active 2')


# -----------
# GET COMMAND
# -----------

# prompting user for next command
if userCommandArray[0].lower() != 'quit':
    userCommand = input("Enter command: ")

userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")

# quit condition
if userCommandArray[0].lower() != 'quit':
#     # Split on String
#     # https://www.tutorialspoint.com/python/string_split.htm
#     # ** break out into function

    print(userCommandArray[1])

    userGetRequest = userCommandArray[1]

    # sending Get command and request for filename to server
    jakeClient.send(userGetRequest.encode())

    # Getting censored message back from server & printing out
    # censoredMessage = jakeClient.recv(70000).decode("utf-8")
    censoredMessage = jakeClient.recv(70000).decode()

    print(censoredMessage)
    print(f"Length of Censored Message 1: {len(censoredMessage)}")
    # Getting Confirmaton of Download from server

    # printing to standard out
    # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    with open(f'client_{userGetRequest}', 'w') as f:
            print(censoredMessage, file=f)

    print(f"Length of Censored Message 2: {len(censoredMessage)}")

        # clean up
    censoredMessage = ''
else:
    print('Quit Statement Active 3')



    # -----------
    # QUIT COMMAND
    # -----------
if userCommandArray[0].lower() != 'quit':
    userCommand = input("Enter command: ")
    print(f"User Command: {userCommand}")
    print("Quitting...")

jakeClient.close()
