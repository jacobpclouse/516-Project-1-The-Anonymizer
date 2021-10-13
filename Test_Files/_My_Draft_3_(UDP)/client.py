''' 
Inspired by the UDP section in the textbook - 2.7
'''

import socket


jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = input('Input lowercase sentence:')
jakeClientUDP.sendto(message.encode(),(socket.gethostname(), 12001))

modifiedMessage, serverAddress = jakeClientUDP.recvfrom(2048)
print(modifiedMessage.decode())

jakeClientUDP.close()