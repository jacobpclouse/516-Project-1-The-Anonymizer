import socket


jakeServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
jakeServerUDP.bind((socket.gethostname(), 12002))

# Server prints this if it has been successfully created
print('The server is ready to receive')


while True:
    # Recieving length check
    sentMessageLength, clientAddress = jakeServerUDP.recvfrom(2048)

    # Putting uncensored text into modified variable
    serverSentMessageLength = sentMessageLength.decode()

    # Print out to check
    print(f"The length of the text sent is {serverSentMessageLength}")

    # Doubling size of message to send back
    serverDoubleMessage = input("Send back to user: ")

    # Getting length of double message
    # from https://www.geeksforgeeks.org/python-string-length-len/
    serverLengthDouble = len(serverDoubleMessage)
    print(f"Double message length is {serverLengthDouble}")

    # Send back to user
    jakeServerUDP.sendto(serverLengthDouble.encode(), clientAddress)
