from socket import *
serverPort = 12000

# create UDP socket
serverSocket= socket(AF_INET, SOCK_DGRAM)

# bind socket to local port number 12000 (this line is incorrect)
serverSocket.bind(("", serverPort))
print("The server is ready to recieve")

# loop forever
while 1:
    # Read from UDP socket into message, getting client’s address (client IP and port)
    message, clientAddress = serverSocket.recvfrom(2048)

    # send upper case string back to this client
    serverSocket.sendto(modifiedMessage, clientAddress)