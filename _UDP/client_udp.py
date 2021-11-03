# THIS USES PYTHON Python 3.8.10
# This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
# No direct lines of code were copied, just used for inspiration
'''
"There is a way out of every box, a solution to every puzzle; it's just a matter of finding it."– Jean-Luc Picard
'''

# Import libraries
import socket
import sys
import time

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


def numOfLoops(lengthVar):
    # find out how many chunks of 1000 you will send, ceiling it
    # https://www.geeksforgeeks.org/floor-ceil-function-python/
    loopsOfChunk1 = float(lengthVar) / 1000
    loopsOfChunkTrunk2 = int(loopsOfChunk1)
    print(loopsOfChunk1)
    print(loopsOfChunkTrunk2)

    #if original value and truncated value are not the same, we will increase truncated value by 1
    if loopsOfChunk1 != loopsOfChunkTrunk2:
        loopsOfChunk1 = loopsOfChunkTrunk2 + 1
        # this will be how many loops we will have to send
    print(f"Expecting {loopsOfChunk1} chunks")
    return loopsOfChunk1


# opens file and gets length
def openTextFile(userCommandArray1):
    filePath = userCommandArray1[1]
    textToChange = open(filePath)
    wholeFileToString1 = textToChange.read()
    textToChange.close()
    return wholeFileToString1


# -----
# Socket Port and IP 

SocketIP = returnIP()
print(SocketIP)

SocketPortNumber = returnPort()
print(SocketPortNumber)

#Setting up socket 
jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ---

# Variables
userCommand = ''
userCommandArray = ['', '']
confirmationServerAck = ''

####
isTimeOut = 0
####



#-------------------------------------
# Main Logic!
#-------------------------------------

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


if userCommandArray[0].lower() == 'put':
    # Getting file length
    wholeFileToString = openTextFile(userCommandArray)

    # Get length
    wholeFileToStringLength = str(len(wholeFileToString))
    print(wholeFileToStringLength)

    # finding number of loops
    loopsOfChunk = numOfLoops(len(wholeFileToString))

    # Sending length of file to server first
    jakeClientUDP.sendto(wholeFileToStringLength.encode(), (SocketIP, SocketPortNumber))
    '''
    LENGTH SEND - NEED ACK OUT AND ACK BACK
    '''
    # timeout for 1 sec
    jakeClientUDP.settimeout(1)

    try:
        # Recieving server ack
        ifAcked, clientAddress = jakeClientUDP.recvfrom(2048)
        ifAcked = ifAcked.decode()
        print(f"From Server: {ifAcked}")
    except:
        # timeout error for no length ack
        print("Did not recieve ACK. Terminating. (Length)")
        isTimeOut = 1
    #reset timeout
    jakeClientUDP.settimeout(None) 

    #cleanup
    ifAcked = ''

    '''
    NEED TO SEND CONF ACK BACK TO SERVER
    '''

    # if timeout check
    if isTimeOut != 1:
        
        outboundChunk = ''
        chunks = 0
        starterPoint = 0

        # WHILE LOOP HERE
        while chunks < loopsOfChunk and isTimeOut != 1:
            endPoint = starterPoint + 1000
            
            # chunking data
            outboundChunk = wholeFileToString[starterPoint:endPoint]

            # Sending Data to Server
            jakeClientUDP.sendto(outboundChunk.encode("utf-8"), (SocketIP, SocketPortNumber))
            '''
            File recieved ACK - Incoming
            '''
            # timeout for 1 sec
            jakeClientUDP.settimeout(1)

            try:
                ifAcked, clientAddress = jakeClientUDP.recvfrom(2048)
                ifAcked = ifAcked.decode()
                print(f"{chunks} From Server: {ifAcked}")
            except:
                # timeout error for no confirmation of data
                print("Did not recieve ACK. Terminating. (File Upload)")
                isTimeOut = 1
            # reset timeout
            jakeClientUDP.settimeout(None) 

            #cleanup
            ifAcked = ''
            outboundChunk = ''
            starterPoint = endPoint
            chunks += 1


        '''
        RECIEVING FIN MESSAGE
        SEND ACK MESSAGE BACK
        '''
        # set timeout to 1 sec

        confirmationServer2 = 'Confirmation Recipt - FIN message'
        jakeClientUDP.settimeout(1)
        
        try:
            ifAcked, clientAddress = jakeClientUDP.recvfrom(2048)
            ifAcked = ifAcked.decode()
            print(ifAcked)
            
            #sending fin recipt back
            jakeClientUDP.sendto(confirmationServer2.encode("utf-8"), (SocketIP, SocketPortNumber))
        except:
            # timeout error for no confirmation of data
            print("Did not recieve ACK. Terminating. (File Upload)")
            isTimeOut = 1

        # reset timout 
        jakeClientUDP.settimeout(None)

        #cleanup
        ifAcked = ''


    else:
        print("Timeout Triggered")

# ----
# # ---------------
# # KEYWORD COMMAND
# # ---------------
# ----
# if timeout check
if isTimeOut != 1:
    # checking to see if quit
    if userCommandArray[0].lower() == 'put':
        userCommand = input("Enter command: ")
        # Split on String
        # https://www.tutorialspoint.com/python/string_split.htm
        userCommandArray = userCommand.split(' ', 1)
        print(f"User command: {userCommandArray[0]}")


    # quit condition (from keyword command input)
    if userCommandArray[0].lower() == 'keyword':
        # specifies phrase to censor & file to have server censor it on
        # sends it to server
        jakeClientUDP.sendto(str(userCommandArray[1]).encode("utf-8"), (SocketIP, SocketPortNumber))
        # Waiting for Server Response
        print("Keyword: Awaiting server response.")
        '''
        TIMEOUT - WAITING FOR ACK BACK
        '''
        jakeClientUDP.settimeout(1)

        try:
            # Recieving confirmation back from server
            confirmationServer1, clientAddress = jakeClientUDP.recvfrom(2048)
            print(confirmationServer1.decode("utf-8"))

        except:
            print("Did not get Keyword Ack Back. Terminating")
            isTimeOut = 1

        # reset timeout
        jakeClientUDP.settimeout(None) 
# ---
                
        '''
        SERVER TIMEOUT - Sending Confirmation of Ack recipt back to server
        '''
        confirmationServer2 = 'Confirmation Recipt - Server Ack'
        jakeClientUDP.sendto((confirmationServer2).encode("utf-8"), (SocketIP, SocketPortNumber)) 


# --

        # getting confirmation that file has been scrambled
        # Getting name of new scrambled file
        # Sending ack back
        confirmationServer1, clientAddress = jakeClientUDP.recvfrom(2048)
        confirmationServer1 = confirmationServer1.decode("utf-8")
        print(f"Server Response: {confirmationServer1}")

        '''
        SENDING ACK to server
        '''
        # message recieved need to send ack to server
        # need to set timeout for incoming ack
        confirmationServer2 = 'Confirmation Recipt - New Anon File Name'
        jakeClientUDP.sendto((confirmationServer2).encode("utf-8"), (SocketIP, SocketPortNumber))

        '''
        TIMEOUT - WAITING FOR ACK OF ACK BACK
        '''
        # Timeout for 1 sec
        jakeClientUDP.settimeout(1)
        
        try:
            # waiting for confirmation from server
            ifAcked, clientAddress = jakeClientUDP.recvfrom(2048)
            ifAcked = ifAcked.decode()
            print(ifAcked)
        except:
            print("Did not get Confirmation Ack Back. Terminating")
            isTimeOut = 1 # will be used to skip other timeouts

        # reset timeout
        jakeClientUDP.settimeout(None)   

        #cleanup
        ifAcked = '' 

else:
    print("Timeout Triggered 2")


# ----
# # -----------
# # GET COMMAND
# # -----------
# ----
# if timeout check
if isTimeOut != 1:
    # prompting user for next command (checks to see if quit active)
    if userCommandArray[0].lower() == 'keyword':
        userCommand = input("Enter command: ")

        # Split on String
        # https://www.tutorialspoint.com/python/string_split.htm
        userCommandArray = userCommand.split(' ', 1)
        print(f"User command: {userCommandArray[0]}")

    # check to see if command is 'get'
    if userCommandArray[0].lower() == 'get':
        
        userGetRequest = str(userCommandArray[1])
        print(f"Sending Request for file: {userGetRequest}")

        # sending Get command and request for filename to server
        jakeClientUDP.sendto(userGetRequest.encode("utf-8"), (SocketIP, SocketPortNumber))

        '''
        TIMEOUT - NEED ACK CONF BACK for Get request
        '''
        # Timeout for 1 sec
        jakeClientUDP.settimeout(1)
        
        try:
            # waiting for ack back from server - get request
            ifAcked, clientAddress = jakeClientUDP.recvfrom(2048)
            ifAcked = ifAcked.decode()
            print(ifAcked)
        except:
            print("Data transmission terminated prematurely.")
            isTimeOut = 1 # will be used to skip other timeouts

        # reset timeout
        jakeClientUDP.settimeout(None)

        #cleanup
        ifAcked = '' 

        '''
        SEND ACK TO SERVER
        '''
        # need to send ack to server
        confirmationServer2 = 'Confirmation Recipt - Get request'
        jakeClientUDP.sendto((confirmationServer2).encode("utf-8"), (SocketIP, SocketPortNumber))

        '''
        TIMEOUT - NEED ACK CONF BACK - Length
        '''
        # Timeout for 1 sec
        jakeClientUDP.settimeout(1)
        
        try:
            # waiting for ack back from server - get request
            serverIncomingLength, clientAddress = jakeClientUDP.recvfrom(2048)
            serverIncomingLength = serverIncomingLength.decode()

        except:
            print("Data transmission terminated prematurely. 2")
            isTimeOut = 1 # will be used to skip other timeouts

        # reset timeout
        jakeClientUDP.settimeout(None)


        '''
        SEND ACK TO SERVER
        '''
        # need to send ack to server
        confirmationServer2 = 'Confirmation Recipt - Length'
        jakeClientUDP.sendto((confirmationServer2).encode("utf-8"), (SocketIP, SocketPortNumber))
# ---


# if timeout check
if isTimeOut != 1 and userCommandArray[0].lower() != 'quit':
    
    # finding number of loops
    loopsOfChunk = numOfLoops(int(serverIncomingLength))
######
    # Going to recieve 
    currentChunkIndex = 0

    # receiving chunks in while loop
    while (currentChunkIndex <= int(loopsOfChunk)) and isTimeOut != 1:
        # Timeout after LEN: need to recieve data before one sec
        jakeClientUDP.settimeout(1)

        try:
            # Recieve incoming data before 1 sec
            confirmationServer1, clientAddress = jakeClientUDP.recvfrom(2048)
            inboundString = confirmationServer1.decode()

            # sending out ACK to client
            serverAckOutbound =  f"Chunk {currentChunkIndex} has been recieved!"
            jakeClientUDP.sendto(serverAckOutbound.encode(), clientAddress)
        except:
            print("Did not recieve data. Terminating")
            isTimeOut = 1 # will be used to skip other timeouts

        # Reset Timeout
        jakeClientUDP.settimeout(None)

        # Writing to file
        if currentChunkIndex == 0:

            # Creating File
            # Overwrite previous file with same name (so we don't accidentally append to it)
            with open(f"{userGetRequest}", 'w') as f:
                print('', end = '', file=f)

        else: 
            #Writing to file
            # https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
            with open(f"{userGetRequest}", 'a') as f:
                print(inboundString, end = '', file=f)

        # cleanup
        confirmationServer1 = ''
        inboundString = ''
        currentChunkIndex += 1 

        # while loop ends ----

    '''
    SENDING FIN MESSAGE
    NEED ACK MESSAGE BACK
    '''
    print(currentChunkIndex) # remove after
    print (loopsOfChunk) # remove
    if (currentChunkIndex - 1 ) == int(loopsOfChunk):
        serverFINMessage = "Server FIN Recieved!"
        
        # Sending Fin message to client
        jakeClientUDP.sendto(serverFINMessage.encode(), clientAddress)

        # Set timeout for 1 sec
        jakeClientUDP.settimeout(1)

        # recieving ack back
        try:
            serverNeedToCensor, clientAddress = jakeClientUDP.recvfrom(2048)
            serverNeedToCensor = serverNeedToCensor.decode()
            print(serverNeedToCensor)
        except:
            print("Data transmission terminated prematurely")
            isTimeOut = 1 # skips other timeouts if 1

        # reset timeout
        jakeClientUDP.settimeout(None)
# ----
# # -----------
# # QUIT COMMAND
# # -----------
# ----
if userCommandArray[0].lower() != 'quit' and isTimeOut != 1:
    print(f"File has been saved as: {userGetRequest}")
    # if timeout check
    if isTimeOut != 1:
        if userCommandArray[0].lower() != 'quit':
            userCommand = input("Enter command: ")
            # Split on String
            # https://www.tutorialspoint.com/python/string_split.htm
            userCommandArray = userCommand.split(' ', 1)
            print(f"User command: {userCommandArray[0]}")

# quit statement
if userCommandArray[0].lower() == 'quit':
    print("Quitting...")
# ---

# closeout
jakeClientUDP.close()

