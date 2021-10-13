#udp client from 516 slides


#include Python’s socket library
from socket import * 
serverName = 'hostname'
serverPort = 12000

# create UDP socket for client
clientSocket = socket(socket.AF_INET, socket.SOCK_DGRAM)

# get user keyboard input
message = raw_input('Input lowercase sentence:')

#Attach server name, port to message; send into socket (might need to change servername and port)
clientSocket.sendto(message, (serverName, serverPort))

#read reply characters from socket into string
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# print out received string and close socket
print(modifiedMessage)
clientSocket.close()