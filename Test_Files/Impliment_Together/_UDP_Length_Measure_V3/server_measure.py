import socket

# --
# Functions
# Help from: https://www.w3schools.com/python/python_functions.asp

# checks cliented reported measurement against actual length
# Might want to impliment a do while loop to query the client if the length is not correct


def checklength(ReportedLength, ActualLength):
    if (ReportedLength) == len(ActualLength):
        print("Lengths match")
        print(f"Message: {ActualLength}")
    else:
        print("LENGTHS DO NOT MATCH")
    # Might have to use a "Do/While Loop to keep querying for resend if message corrupted"
# --
portNum = 12002
socketNum = socket.gethostname()


jakeServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
jakeServerUDP.bind((socketNum, portNum))

# Server prints this if it has been successfully created
print('The server is ready to receive')

while True:
    # Recieving length check
    sentMessageLength, clientAddress = jakeServerUDP.recvfrom(2048)

    # Putting length Check into variable
    # In order to use this, will need to convert from string to int
    serverSentMessageLength = int(sentMessageLength.decode())

# --

    # Recieving actual text
    sentMessageContent, clientAddress = jakeServerUDP.recvfrom(2048)

    # Putting message content into variable
    serverSentMessageContent = sentMessageContent.decode()

# --
    # Need to see if the sent length and actual length are equivalent
    checklength(serverSentMessageLength, serverSentMessageContent)

# --

    # Print out to check
    print(f"The length of the text sent is {serverSentMessageLength}")



# --


    # creating message to send back to client
    serverMessageToUser = input("Send back to user: ")


# --

    # Getting length of message and converting to str
    # from https://www.geeksforgeeks.org/python-string-length-len/
    serverLengthToClient = str(len(serverMessageToUser))
    print(f"Server Message length is {serverLengthToClient}")

    # Send back Length to user
    jakeServerUDP.sendto(serverLengthToClient.encode(), clientAddress)

# --

    # Sending actual message client 
    jakeServerUDP.sendto(serverMessageToUser.encode(), clientAddress)
