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


# put /media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/Test_Files/UncensoredText/uncensored.txt
# put /media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/_TCP_Final/uncensored_text.txt
# put uncensored_text.txt


# Import libraries
import socket
import sys


# importing Command line arguments - for port number
# https://cs.stanford.edu/people/nick/py/python-main.html

def returnPort():
    inputVar = int(sys.argv[1])
    return inputVar
    # Return Statement in function to return value
    # https://www.w3schools.com/python/python_functions.asp



SocketIP = socket.gethostname()
SocketPortNumber = returnPort()
# SocketPortNumber = int(input("Give me a port Number: "))

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeClient.connect((SocketIP, SocketPortNumber))

# ---

# Variables
userCommand = ''

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
textToChange = open(userCommandArray[1])
wholeFileToString = textToChange.read()
textToChange.close()

print(wholeFileToString)

# sending put string to server
# assuming first string is always 'put'
jakeClient.send(wholeFileToString.encode())


userCommand = ''
userCommandArray = []

# ---


    # prompting user for next command
while userCommand == '':
    userCommand = input("Waiting for Keyword command: ")

    if userCommand.lower() == 'quit':
        break

    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    # ** break out into function
userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")


# -- 

# 'keyword' command
# specifies phrase to censor AND file to censor the word in
userCensorPhraseNFile = userCommandArray[1]

print(userCensorPhraseNFile)

# sending keyword phrase and filename to operate on to server
# assuming second string is always 'keyword'
jakeClient.send(userCensorPhraseNFile.encode())

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
jakeClient.send(userGetRequest.encode())


# --

#Getting censored message back from server & printing out
censoredMessage = jakeClient.recv(2048)
print(f'From Server: {censoredMessage.decode()}')


#---

# printing to standard out
# from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
with open(f'./OutputText/{userGetRequestFilePath}.txt', 'w') as f:
    print(censoredMessage, file=f)


jakeClient.close()


# MIGHT NEED TO CHECK FOR SPACES ON EACH SIDE! IT CENSORS ANYTHING THAT HAS THE LETTER IN IT
# ALSO TRY TO USE FUNCTIONS AS WELL
# CHECK WHAT SHE MEANS BY THE 'GET' COMMAND