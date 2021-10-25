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

# put File1.txt
# keyword ICSI File1.txt
# get AnonFile1.txt



# put ./ZInputText/File1.txt

# keyword Project ./ZInputText/File1.txt

# keyword Fall ./OutputText/ZInputText/File1.txt
    # will recieve filename back from server

# get File1.txt




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



#SocketIP = socket.gethostname()
SocketIP = returnIP()
print(SocketIP)
SocketPortNumber = returnPort()
print(SocketPortNumber)

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeClient.connect((SocketIP, SocketPortNumber))

# ---

# Variables
userCommand = ''

# ---

# Main Logic!
    # try breaking this out into its own function if it works (then can call it)
    # ** Might try having the entire function under this command if it works (empty string)

# -----------
# PUT COMMAND
# -----------


while userCommand == '':
    userCommand = input("Enter Command: ")

    if userCommand.lower() == 'quit':
        break

    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    # ** break out into function
userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")


# opening file
# https://docs.python.org/3/library/functions.html#open
filePath = userCommandArray[1]
textToChange = open(filePath)
wholeFileToString = textToChange.read()
textToChange.close()


print(f"The length of the file is: {len(wholeFileToString)}")


# sending original filename to server
jakeClient.send(filePath.encode())

# sending put string to server
# assuming first string is always 'put'
jakeClient.send(wholeFileToString.encode())
print("Awaiting Server Response")


# Recieving confirmation back from server
confirmationServer1 = jakeClient.recv(2048).decode("utf-8")
print(confirmationServer1)


# cleaning up
userCommand = ''
userCommandArray = []
confirmationServer1 = ''

# # ---


# ---------------
# KEYWORD COMMAND
# ---------------


# prompting user for next command
while userCommand == '':
    userCommand = input("Enter command: ")

    if userCommand.lower() == 'quit':
        break

#     # Split on String
#     # https://www.tutorialspoint.com/python/string_split.htm
#     # ** break out into function
userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")
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

# # Storing new file name in variable
#newCensoredFileName = jakeClient.recv(2048).decode("utf-8")

# cleaning up
userCommand = ''
userCommandArray = []
confirmationServer1 = ''




# -----------
# GET COMMAND
# -----------

# prompting user for next command
while userCommand == '':
    userCommand = input("Enter command: ")

    if userCommand.lower() == 'quit':
        break

#     # Split on String
#     # https://www.tutorialspoint.com/python/string_split.htm
#     # ** break out into function
userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")
print(userCommandArray[1])

userGetRequest = userCommandArray[1]


# sending Get command and request for filename to server
jakeClient.send(userGetRequest.encode())

# Getting censored message back from server & printing out
censoredMessage = jakeClient.recv(65527).decode("utf-8")

print(censoredMessage)

# Getting Confirmaton of Download from server
# print(f'From Server: {censoredMessage.decode()}')


# printing to standard out
# from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
with open(f'client_{userGetRequest}', 'w') as f:
    print(censoredMessage, file=f)

jakeClient.close()


