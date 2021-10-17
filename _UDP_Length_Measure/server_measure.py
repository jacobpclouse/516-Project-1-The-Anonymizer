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


jakeServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
jakeServerUDP.bind((socket.gethostname(), 12002))

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


    # Doubling size of message to send back
    serverDoubleMessage = input("Send back to user: ")


# --

    # Getting length of double message
    # from https://www.geeksforgeeks.org/python-string-length-len/
    serverLengthDouble = str(len(serverDoubleMessage))
    print(f"Server Message length is {serverLengthDouble}")

    # Send back to user
    jakeServerUDP.sendto(serverLengthDouble.encode(), clientAddress)
