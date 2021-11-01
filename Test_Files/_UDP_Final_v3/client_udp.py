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



# -----
# Socket Port and IP 

SocketIP = returnIP()
#SocketIP = socket.gethostname()
print(SocketIP)
SocketPortNumber = returnPort()
print(SocketPortNumber)

#Setting up socket 
jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ---

# Variables
userCommand = ''
userCommandArray = ['', '']
lengthOfChunk = 1000
getLengthOfChunk = 1000

# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []
chunkBookmark = 0

# ---

# Main Logic!

# ----
# # -----------
# # PUT COMMAND
# # -----------
# ----
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

    wholeFileToString.strip()

    # -----------
    # Need To Send Length to server
    # -----------
    # Store Length to a variable
    fileLengthVar = len(wholeFileToString)
    wholeFileToStringLength = f"LEN:{(fileLengthVar)}"
    print(f"The length of the file is: {wholeFileToStringLength}")

    # Sending length of file to server first
    jakeClientUDP.sendto(wholeFileToStringLength.encode(), (SocketIP, SocketPortNumber))

    # find out how many chunks of 1000 you will send, ceiling it
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

    # ----
    # Chunk String
    # ----
    # append info to array
    # https://www.freecodecamp.org/news/python-list-append-how-to-add-an-element-to-an-array-explained-with-examples/
    user1000ByteArray = []

    chunks = 0
    starterPoint = 0
    while chunks < loopsOfChunk:
        
        endPoint = starterPoint + lengthOfChunk
        # appending
        user1000ByteArray.append(wholeFileToString[starterPoint:endPoint])

        print(f"On chunk: {chunks}, String to append is: {wholeFileToString[starterPoint:endPoint]}")
        print("Array currently is:")
        print(user1000ByteArray)

        starterPoint = endPoint
        chunks += 1


    #----
    # Sending over server chunks
    # Waiting for server response
    #----

        # should start at user1000ByteArray[0]
        # should end at user1000ByteArray[loopsOfChunk]
    
    currentChunkIndex = 0
    ifAcked = ''
    numChunksRecived = 0

    while currentChunkIndex < loopsOfChunk:
        print(f"On Array Section {currentChunkIndex}")


        #Sending to server
        outboundString = str(user1000ByteArray[currentChunkIndex])
        print(outboundString)
        jakeClientUDP.sendto(outboundString.encode("utf-8"), (SocketIP, SocketPortNumber))

        # wait for ACK

        print("Waiting for ACK")
        ifAcked, clientAddress = jakeClientUDP.recvfrom(2048)
        ifAcked = ifAcked.decode("utf-8")
        print(f"Server Says: {ifAcked}")

        # incriment
        currentChunkIndex += 1
        numChunksRecived +=1

        # clean up
        ifAcked = ''

    print(numChunksRecived)
    
    # Need to wait until recieve FIN Message from 
    ##TIMEOUT NEEDED
    ifFin = ''
    print("Waiting for FIN")
    ifFin, clientAddress = jakeClientUDP.recvfrom(2048)
    ifFin = ifFin.decode()
    print(f"Server Response: {ifFin}")


    
# ----
# # ---------------
# # KEYWORD COMMAND
# # ---------------
# ----

# prompting user for next command
# also checking to see if quit command is not already active
if userCommandArray[0].lower() != 'quit':
    userCommand = input("Enter command: ")

    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    userCommandArray = userCommand.split(' ', 1)
    print(f"User command: {userCommandArray[0]}")

# quit condition (from keyword command input)
if userCommandArray[0].lower() != 'quit':
    print(userCommandArray[1])

    # specifies phrase to censor & file to have server censor it on
    # sends it to server
    #userCensorPhrase = userCommandArray[1]
    jakeClientUDP.sendto(str(userCommandArray[1]).encode("utf-8"), (SocketIP, SocketPortNumber))

    # Waiting for Server Response
    print("Awaiting server response.")

    # Recieving confirmation back from server
    confirmationServer1, serverAddress = jakeClientUDP.recvfrom(2048)
    print(confirmationServer1.decode("utf-8"))

    # cleaning up
    userCommand = ''
    userCommandArray = ['', '']
    confirmationServer1 = ''
else:
    print('Quit Statement Active')


# ----
# # -----------
# # GET COMMAND
# # -----------
# ----

# prompting user for next command
if userCommandArray[0].lower() != 'quit':
    userCommand = input("Enter command: ")

userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")

# quit condition
if userCommandArray[0].lower() != 'quit':
    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm

    userGetRequest = str(userCommandArray[1])
    print(f"Sending Request for file: {userGetRequest}")

    

    # sending Get command and request for filename to server
    jakeClientUDP.sendto(userGetRequest.encode("utf-8"), (SocketIP, SocketPortNumber))


    # Need to accept and print out length of incoming string
    # Decoding and pushing it through to array, then displaying
    incomingStringLength, clientAddress = jakeClientUDP.recvfrom(2048)
    incomingStringLength = incomingStringLength.decode("utf-8")

    incomingStringLengthArray = (incomingStringLength).split(':', 1)
    print(incomingStringLengthArray)
    print(f"According to server, The length of the file is: {incomingStringLengthArray[1]}")
    # TIMEOUT NEEDED IF LENGTH NOT RECIEVED
# ----

    # find out how many chunks of 1000 you will send, ceiling it
    # https://www.geeksforgeeks.org/floor-ceil-function-python/
    #getLengthOfChunk = 1000
    getLoopsOfChunk = float(incomingStringLengthArray[1]) / getLengthOfChunk
    getLoopsOfChunkTrunk = int(getLoopsOfChunk)
    print(getLoopsOfChunk)
    print(getLoopsOfChunkTrunk)

    #if original value and truncated value are not the same, we will increase truncated value by 1
    if getLoopsOfChunk != getLoopsOfChunkTrunk:
        getLoopsOfChunk = getLoopsOfChunkTrunk + 1
        # this will be how many loops we will have to send
    print(f"Expecting {getLoopsOfChunk} chunks")


# -----

    # Creating String to write recive from 
    clientCensoredMessage = ''

    # Going to recieve 
    clientCurrentChunkIndex = 0
    clientAckOutbound = "Chunk has been recieved!"

    while clientCurrentChunkIndex < getLoopsOfChunk:
        print(f"On Array Section {clientCurrentChunkIndex}")


        # Recieving string in 1000 byte incriments
        clientCensoredMessage, clientAddress = jakeClientUDP.recvfrom(65527)
        clientInboundString = clientCensoredMessage.decode("utf-8")
        

        # Sending ACK
        jakeClientUDP.sendto(clientAckOutbound.encode("utf-8"), (SocketIP, SocketPortNumber))



        if clientCurrentChunkIndex == 0:

            # Creating File
            # Overwrite previous file with same name (so we don't accidentally append to it)
            with open(f"client_{userGetRequest}", 'w') as f:
                print(clientInboundString, file=f)

            # cleanup
            clientInboundString = ''
                
            
        else:

            #Writing to file
            # https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
            with open(f"client_{userGetRequest}", 'a') as f:
                print(clientInboundString, file=f)
        

        # incriment
        clientCurrentChunkIndex += 1 

        # cleanup
        clientInboundString = ''

        


    # Send Fin String to client
    finMessageToServer = 'Full Message Recieved!'
    jakeClientUDP.sendto(finMessageToServer.encode("utf-8"), (SocketIP, SocketPortNumber))





# -----------
# QUIT COMMAND
# -----------
print(f"File has been saved as: client_{userGetRequest}")

if userCommandArray[0].lower() != 'quit':
    userCommand = input("Enter command: ")
    print(f"User Command: {userCommand}")
    print("Quitting...")
'''
# jakeClientUDP.close()
'''


