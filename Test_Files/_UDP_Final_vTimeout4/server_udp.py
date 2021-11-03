# THIS USES PYTHON Python 3.8.10

'''
 This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
 
 Questions: 
 
 10) the timeout after length and ack are kinda fused together, is that alright?

 11) Do you want a timeout for the FIN message as well? Or is it just ACK messages?

 12) I use an array to split up my data, but it gives me new lines that break up phrases. How do i remove them?
 
 13) *** Have her take a look at timeouts and make sure that you are doing them correctly***
    POST QUESTIONS IN FORUM


14) Am I chunking the string up correctly? Ie: it am use 1000 for my segment size, but I don't know if that is sans header


*** MAKE SURE THAT THE SERVER CODE KEEPS RUNNIN NO MATTER WHAT (Ie: timeouts, incorrect code, etc)
 '''

# -----------------------------------
# -----------------------------------

# Import libraries
import socket
import sys


# --
# Functions

# Gets length of string and creates the character to replace it with
def myFindTargetString(targetPhase):
    replacementString = ''
    replacementChar = 'X'
    for letters in targetPhase:
        replacementString += replacementChar
    return replacementString



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
print(SocketIP)

SocketPortNumber = returnPort()
print(SocketPortNumber)



# Main Logic
# ---

jakeServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
jakeServerUDP.bind((SocketIP, SocketPortNumber))



# --


# Variables
serverNeedToCensor = ''
serverSecretPhrase = ''
lengthOfChunk = 1000
lengthOfChunkOutbound = 1000

# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []
chunkBookmark = 0



# added

recievedSuccessfully = 'Data Recieved'

serverNeedToCensorLength = ''
serverNeedToCensorLengthArray = ['', '']

serverOriginalFileName = ''
serverCensoredName = ''

serverNeedToCensor = ''

serverKeywordData = 'default value'
serverKeywordFileName = ''

serverGetRequest = ''

serverFinalText = ''


# ---
# Program logic
# ---


# shows server is up and running
print("Server Is Online")


# going to get data from client, loop until manually stoped
while True:

    # Server prints this if it has been successfully created
    print(f'The server is ready to receive on Hostname: {SocketIP}, Port: {SocketPortNumber}')

#     # -----------
#     # PUT COMMAND
#     # -----------

    # Need to accept and print out length of incoming string
    # Decoding and pushing it through to array, then displaying
    serverNeedToCensorLength, clientAddress = jakeServerUDP.recvfrom(2048)
    serverNeedToCensorLength = serverNeedToCensorLength.decode()
    serverNeedToCensorLengthArray = (serverNeedToCensorLength).split(':', 1)
    print(serverNeedToCensorLengthArray)
    print(f"According to client, The length of the file is: {serverNeedToCensorLengthArray[1]}")


    # timing out if response is not recieved after 1 second
    # From https://docs.python.org/3/library/socket.html#socket.socket.settimeout
    #jakeServerUDP.settimeout(1)
    

        # letting client know that length was recieved correctly
    jakeServerUDP.sendto(recievedSuccessfully.encode(), clientAddress)





    # find out how many chunks of 1000 you will send, ceiling it
    # https://www.geeksforgeeks.org/floor-ceil-function-python/
    #lengthOfChunk = 1000
    loopsOfChunk = float(serverNeedToCensorLengthArray[1]) / lengthOfChunk
    loopsOfChunkTrunk = int(loopsOfChunk)
    print(loopsOfChunk)
    print(loopsOfChunkTrunk)

    #if original value and truncated value are not the same, we will increase truncated value by 1
    if loopsOfChunk != loopsOfChunkTrunk:
        loopsOfChunk = loopsOfChunkTrunk + 1
        # this will be how many loops we will have to send
    print(f"Expecting {loopsOfChunk} chunks")


    # Creating String to write recive from 
    serverNeedToCensor = ''

    # Going to recieve 
    currentChunkIndex = 0
    serverAckOutbound = "Chunk has been recieved!"

    
    while currentChunkIndex < loopsOfChunk:
        print(f"On Array Section {currentChunkIndex}")
        jakeServerUDP.settimeout(1)

        try:
            # Recieving string in 1000 byte incriments
            serverNeedToCensor, clientAddress = jakeServerUDP.recvfrom(65527)
            inboundString = serverNeedToCensor.decode("utf-8")

            # Timeout in 1 sec
            #jakeServerUDP.settimeout(1)
            
        except:
            # Printing out error
            print("Did not recieve data. Terminating")
            break
        
        # reset timeout
        # Help from Lav at https://stackoverflow.com/questions/34371096/how-to-use-python-socket-settimeout-properly
        jakeServerUDP.settimeout(None)


        # Sending ACK
        jakeServerUDP.sendto(serverAckOutbound.encode(), clientAddress)


        # Server Side File Storage
        ServerSideFileName = "ServerSideFile__" + str(loopsOfChunk)


        if currentChunkIndex == 0:

            # Creating File
            # Overwrite previous file with same name (so we don't accidentally append to it)
            with open(f"{ServerSideFileName}", 'w') as f:
                # will print to file WITHOUT Adding a newline at the end!
                # https://careerkarma.com/blog/python-print-without-new-line/
                print(inboundString, end = '', file=f)

            # cleanup
            inboundString = ''
            
                
            
        else:

            #Writing to file
        # https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
        # https://stackoverflow.com/questions/42912098/removing-a-specific-character-from-a-text-file
            with open(f"{ServerSideFileName}", 'a') as f:
                # will print to file WITHOUT Adding a newline at the end!
                # https://careerkarma.com/blog/python-print-without-new-line/
                print(inboundString, end = '', file=f)
        

        # incriment
        currentChunkIndex += 1 

        # cleanup
        inboundString = ''
       


    # Send Fin String to client
    finMessageToClient = 'Progress To Next Step'

    # checking to see if the number of chunks we got was equal to the number we expected
    if currentChunkIndex == loopsOfChunk:
        print("Number of Chunks Recieved == Number of Chunks Expected")
    
        jakeServerUDP.sendto(finMessageToClient.encode(), clientAddress)



    # ---------------
    # KEYWORD COMMAND
    # ---------------

    # Accepting the word to censor from client
    # AND target file's filename from client

    serverKeywordData, clientAddress = jakeServerUDP.recvfrom(2048)
    serverKeywordArray = (serverKeywordData.decode()).split(' ', 1)

    # Getting Phase to Censor
    serverSecretPhrase = serverKeywordArray[0]
    print(f"Top Secret Word to censor is: {serverSecretPhrase}")


    # Getting Original Name of file, will use to rename new text
            # check to see if serverKeywordArray[1] exits with if statement
    serverKeywordFileName = serverKeywordArray[1]
    print(f"Keyword Filename: {serverKeywordFileName}")
    serverCensoredName = "Anon_UDP_" + str(serverKeywordFileName)
    print(serverCensoredName)

    # creating string to replace target phrase with
    serverReplacementString = myFindTargetString(serverSecretPhrase)
    print(f"Replacement String will be: {serverReplacementString}")


    # opening new anon file
    # https://docs.python.org/3/library/functions.html#open
    textToChange = open(f"{ServerSideFileName}")
    serverWholeFileToString = textToChange.read()
    textToChange.close()


# # --------------------------##
#      Anonymize Logic here    #
# # --------------------------##


    # Doing find and replace
    # from https://www.geeksforgeeks.org/python-string-replace/
    serverCensoredOutput = serverWholeFileToString.replace(
        serverSecretPhrase, serverReplacementString)

    
    # Overwriting any previous file with the same name
    f = open(f"{serverCensoredName}", "w")

    # Output sting to file
    # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
    
    with open(f"{serverCensoredName}", 'a') as f:
        print(serverCensoredOutput, file=f)


    
    # send response back to client
    # Sending back name of the new censored file
    messageRecieved = f"Server response: File {serverKeywordFileName} has been anonymized. Output file is {serverCensoredName}"
    print(messageRecieved)
    jakeServerUDP.sendto(messageRecieved.encode(), clientAddress)


    # -----------
    # Need To Determine Length of string to Send to client
    # Will Send to Client after GET request
    # -----------

    # Store Length to a variable
    fileLengthVar = len(serverCensoredOutput)
    wholeFileToStringLength = f"LEN:{(fileLengthVar)}" #***SEND THIS TO CLIENT
    print(f"The length of the file is: {wholeFileToStringLength}")

    # find out how many chunks of 1000 you will send, ceiling it
    # https://www.geeksforgeeks.org/floor-ceil-function-python/
    #lengthOfChunkOutbound = 1000
    loopsOfChunkOutbound = fileLengthVar / lengthOfChunkOutbound
    loopsOfChunkOutboundTrunk = int(loopsOfChunkOutbound)
    print(loopsOfChunkOutbound)
    print(loopsOfChunkOutboundTrunk)

    #if original value and truncated value are not the same, we will increase truncated value by 1
    if loopsOfChunkOutbound != loopsOfChunkOutboundTrunk:
        loopsOfChunkOutbound = loopsOfChunkOutboundTrunk + 1
        # this will be how many loops we will have to send
    print(f"Expect {loopsOfChunkOutbound} loops")



# ------

    # -----------
    # GET COMMAND
    # -----------

    # Recieving Get request from user
    serverGetRequest, clientAddress = jakeServerUDP.recvfrom(2048)
    serverGetRequest = serverGetRequest.decode("utf-8")
    print(f"Get Request Recieved: {serverGetRequest}")

    # Sending length of file to client first
    jakeServerUDP.sendto(wholeFileToStringLength.encode(), clientAddress)
    print("Length Var Sent to Client")



    # ----
    # Chunk String
    # ----
    # append info to array
    # https://www.freecodecamp.org/news/python-list-append-how-to-add-an-element-to-an-array-explained-with-examples/
    user1000ByteArray = []

    chunks = 0
    starterPoint = 0
    while chunks < loopsOfChunkOutbound:
        
        endPoint = starterPoint + lengthOfChunk
        # appending
        user1000ByteArray.append(serverCensoredOutput[starterPoint:endPoint])

        print(f"On chunk: {chunks}, String to append is: {serverCensoredOutput[starterPoint:endPoint]}")
        print("Array currently is:")
        print(user1000ByteArray)

        starterPoint = endPoint
        chunks += 1

    print("Got through Array If you see this")

# -----
    #----
    # Sending over client chunks
    # Waiting for client response
    #----

        # should start at user1000ByteArray[0]
        # should end at user1000ByteArray[loopsOfChunkOutbound]
   
    serverCurrentChunkIndex = 0
    ifAcked = ''
    numChunksRecived = 0

    while serverCurrentChunkIndex < loopsOfChunkOutbound:
        print(f"On Array Section {serverCurrentChunkIndex}")


        #Sending to client
        outboundString = str(user1000ByteArray[serverCurrentChunkIndex])
        print(outboundString)
        jakeServerUDP.sendto(outboundString.encode("utf-8"), clientAddress)

        
        jakeServerUDP.settimeout(1)
        try:
            # wait for ACK

            print("Waiting for ACK")
            ifAcked, clientAddress = jakeServerUDP.recvfrom(2048)
            ifAcked = ifAcked.decode("utf-8")
            print(f"Server Says: {ifAcked}")

            # incriment
            serverCurrentChunkIndex += 1
            numChunksRecived +=1

            # clean up
            ifAcked = ''

            # Setting timeout for 1 second, looking for ACK
             # Help from Lav at https://stackoverflow.com/questions/34371096/how-to-use-python-socket-settimeout-properly
            #jakeServerUDP.settimeout(1)
        except:
            print("Did not recieve Ack. Terminating.")
            break


        # Reseting Timeout in loop
        # Help from Lav at https://stackoverflow.com/questions/34371096/how-to-use-python-socket-settimeout-properly
        jakeServerUDP.settimeout(None)

    print(numChunksRecived)
    

    # Reseting Timeout after loop
    # Help from Lav at https://stackoverflow.com/questions/34371096/how-to-use-python-socket-settimeout-properly
    jakeServerUDP.settimeout(None)


    # Need to wait until recieve FIN Message from 
    ifFin = ''
    print("Waiting for FIN")
    ifFin, clientAddress = jakeServerUDP.recvfrom(2048)
    ifFin = ifFin.decode()
    print(f"Client Response: {ifFin}")


# If you read all the comments up to here, man that is some dedication
# The gang of Sesame Street wants to congradulate you:

'''
   . -- .
  (      )
 ( (/oo\) )
  ( \''/ )                               WW
   ( \/ )      wwwwww                   /__\
  (      )   w"ww  ww"w                | oo |   _WWWWW_
 (        ) W   o""o   W    (o)(o)    (|_()_|) /  o o  \   (+)(+)
(          )W  ______  W  w"      "w    \__/ (|  __O__  |)/      \
 (        ) "w \_\/_/ w" W  -====-  W  /|\/|\  \ \___/ /  \ -==- /
   ' -- '  ww""wwwwww""ww "w      w"  |||||||| /-------\   \    /
    =  =    |||||||||||| w""""""""""w |||||||||=========| <\/\/\/>
    =  =    ||||||||||||W            W|||||||||=========| /      \
'''

# ASCII Art from ASCII Art Archive @ https://www.asciiart.eu/television/sesame-street
