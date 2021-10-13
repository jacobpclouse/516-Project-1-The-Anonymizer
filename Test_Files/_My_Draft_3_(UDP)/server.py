''' 
Inspired by the UDP section in the textbook - 2.7
'''

import socket


jakeServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
jakeServerUDP.bind((socket.gethostname(), 12001))


print('The server is ready to receive')

while True:
    message, clientAddress = jakeServerUDP.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    jakeServerUDP.sendto(modifiedMessage.encode(), clientAddress)