import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((socket.gethostname(), 12000))

'''
serverPort = 12000

# create UDP socket
serverSocket= socket(AF_INET, SOCK_DGRAM)

# bind socket to local port number 12000 (this line is incorrect)
serverSocket.bind((socket.gethostname(), serverPort))
'''

print("The server is ready to recieve")
print(socket.gethostname())

# loop forever
while 1:
    clientsocket, address = serverSocket.accept()
    # Read from UDP socket into message, getting client’s address (client IP and port)
    message, clientAddress = serverSocket.recvfrom(2048)

    # send upper case string back to this client
    serverSocket.sendto(modifiedMessage, clientAddress)