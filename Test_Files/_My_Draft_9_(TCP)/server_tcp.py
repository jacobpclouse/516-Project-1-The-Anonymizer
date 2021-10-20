'''
 This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
 
 Questions: 
 1) I am getting this error on longer files that I want to convert: OSError: [Errno 9] Bad file descriptor
    I had issues with longer files as well as single line files (doesn't look like size)
    Does it have to do with timeout not being set?
 '''
# Socket Stuff
import socket

SocketIP = socket.gethostname()
SocketPortNumber = 12002

jakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
jakeServer.bind((SocketIP, SocketPortNumber))


# Variables
serverNeedToCensor = ''
serverSecretPhrase = ''

# ---

# Functions


def cleanUp(stringToWipe, stringToWipe2):
    stringToWipe = ''
    stringToWipe2 = ''
    print(f"{stringToWipe, stringToWipe2} have been wiped")


# ---

# Program logic
# shows server is up and running
print("The server is ready to receive")

# buffer set to 5
jakeServer.listen(5)


# going to get data from client, look at the start and see what keyword it has
while True:
    clientSocket, clientAddress = jakeServer.accept()
    print(f"Connection from {clientAddress} has been established.")

    # Getting command from client
    incomingCommand = clientSocket.recv(2048).decode()
    print(incomingCommand)
   


    '''
 # Getting data from client
    incomingData = clientSocket.recv(2048).decode()
    print(incomingData)


    # should loop until both fields are filled
    while serverNeedToCensor == '' and serverSecretPhrase == '':

        # Getting command from client
        incomingCommand = clientSocket.recv(2048).decode()
        # Getting data from client
        incomingData = clientSocket.recv(2048).decode()

        if incomingCommand == 'put':
            # putting text to censor in variable
            serverNeedToCensor = incomingData
            print("Put Command recieved: Have string to censor:")
            # cleaning up
            cleanUp(incomingCommand, incomingData)

        elif incomingCommand == 'key':
            # loggin keyword to censor into variable
            serverSecretPhrase = incomingData
            print(f"Keyword Recieved: {serverSecretPhrase}")
            # cleaning up
            cleanUp(incomingCommand, incomingData)

    print("Both string and keyword have been recieved")
'''

'''

    # ---
    # Accepting String that needs to be censored from client
    serverNeedToCensor = clientSocket.recv(2048).decode()
    print(f"String that needs to be censored is {serverNeedToCensor}")

    # ---
    # Accepting the Top Secret Word to censor from client
    serverSecretPhrase = clientSocket.recv(2048).decode()
    print(f"Top Secret Word to censor is {serverSecretPhrase}")

    # ---
    # Accepting the replacement character to censor from client
    serverReplacementChar = clientSocket.recv(2048).decode()
    print(f"the replacement character is {serverReplacementChar}")

    # ---
    # Displaying output
    print(
        f"RECIEVED {serverNeedToCensor, serverSecretPhrase, serverReplacementChar} FROM {clientAddress}")

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


    # Creating the data to send back to client
    clientSocket.send(censoredOutput.encode())

    # ---
'''
