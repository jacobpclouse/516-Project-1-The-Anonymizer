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


SocketIP = returnIP()
print(SocketIP)
SocketPortNumber = returnPort()
print(SocketPortNumber)

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeClient.connect((SocketIP, SocketPortNumber))

# ---

# Variables
userCommand = ''
userCommandArray = ['', '']

lengthOfChunk = 4000
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
    print(f"The length of the file is: {fileLengthVar}")

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
    print(loopsOfChunk)
    print(loopsOfChunkTrunk)

    #if original value and truncated value are not the same, we will increase truncated value by 1
    if loopsOfChunk != loopsOfChunkTrunk:
        loopsOfChunk = loopsOfChunkTrunk + 1
        # this will be how many loops we will have to send
    print(f"Expect {loopsOfChunk} loops")

    # converting to string for ease
    outboundLoops = str(loopsOfChunk)

    # Sending number of chunks to server first
    jakeClient.send(outboundLoops.encode())
    print(outboundLoops)


    # Recieving ACK
    clientAck, clientAddress = jakeClient.recvfrom(2048)
    print(f"Server Length Response: {clientAck}")

    # ----
    # Chunk String, Send Out
    # ----
    outboundChunk = ''

    chunks = 0
    starterPoint = 0
    while chunks < loopsOfChunk:

        endPoint = starterPoint + lengthOfChunk

        # Sending
        jakeClient.send(wholeFileToString[starterPoint:endPoint].encode())


        print(f"On chunk: {chunks}, String to append is: {wholeFileToString[starterPoint:endPoint]}")

        starterPoint = endPoint
        chunks += 1


        # # wait for ACK

        print("Waiting for ACK")

        # # Recieving ACK from Server
        ifAcked, clientAddress = jakeClient.recvfrom(2048)
        ifAcked = ifAcked.decode("utf-8")

        print(f"Server Says: {ifAcked}")


        # # clean up
        ifAcked = ''




    # cleaning up
    userCommand = ''
    confirmationServer1 = ''

# # ---



# ---------------
# KEYWORD COMMAND
# ---------------
    # prompting user for next command
    userCommand = input("Enter command: ")
    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    userCommandArray = userCommand.split(' ', 1)
    print(f"User command: {userCommandArray[0]}")


# also checking to see if quit command is not active
if userCommandArray[0].lower()  == 'keyword':
    
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
    #try commenting print ack out  if it doesn't work

    # cleaning up
    userCommand = ''
    userCommandArray = ['', '']
    confirmationServer1 = ''



# -----------
# GET COMMAND
# -----------

    # prompting user for next command
    userCommand = input("Enter command: ")
#     # Split on String
#     # https://www.tutorialspoint.com/python/string_split.htm
    userCommandArray = userCommand.split(' ', 1)
    print(f"User command: {userCommandArray[0]}")


if userCommandArray[0].lower() == 'get':
    
    print(userCommandArray[1])

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
    censoredTextFileName = f"client_Anon{filePath}"


    while currentChunkIndex <= int(loopsOfChunk):
        print(f"On String Section Section {currentChunkIndex}")
        print(f"Need to get to {int(loopsOfChunk)}")

        # Recieving string in byte incriments
        censoredMessage = jakeClient.recv(65000)
        censoredMessage = censoredMessage.decode("utf-8")
        print(censoredMessage)

        # creating ACK
        serverAckOutbound =  f"Chunk {currentChunkIndex} has been recieved!"

        if currentChunkIndex == 0:

            # Creating File
            # Overwrite previous file with same name (so we don't accidentally append to it)
            #with open(f"{censoredTextFileName}", 'w') as f:
            #     print(censoredMessage, end = '', file=f)

            # print("1st statement")
            print(censoredMessage)
            

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
        
            print("2nd Statement")
            # incriment
            currentChunkIndex += 1 

            # cleanup
            censoredMessage = ''

            # Sending Ack
            jakeClient.send(serverAckOutbound.encode())

     # Sending ACK
    jakeClient.send(serverAckOutbound.encode())

    print("Done with Recieving!")


###### ----------
    # Getting censored message back from server & printing out
    #censoredMessage = jakeClient.recv(100000).decode()

    # print(censoredMessage)
    # print(f"Length of Censored Message 1: {len(censoredMessage)}")
    # # Getting Confirmaton of Download from server

    # # printing to standard out
    # # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    # with open(f'client_{userGetRequest}', 'w') as f:
    #         print(censoredMessage, file=f)

    # print(f"Length of Censored Message 2: {len(censoredMessage)}")
    # print(f"Message has been downloaded and stored as: client_{userGetRequest}")

    #     # clean up
    # censoredMessage = ''

# ---



# -----------
# QUIT COMMAND
# -----------
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
