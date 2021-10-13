'''
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1235))

msg = s.recv(1024)
print(msg.decode("utf-8"))

This was taken from https://pythonprogramming.net/sockets-tutorial-python-3/ '''

import socket

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#jakeClient.connect((socket.gethostname(), 12000))
jakeClient.connect((socket.gethostname(), 12000))



OutboundMessage = input("Give me a number")
jakeClient.send(OutboundMessage.encode())

IncomingMessage = jakeClient.recv(2048)
print(f'From Server: {IncomingMessage.decode()}')

jakeClient.close()



#msg = jakeClient.recv(1024)
#print(msg.decode("utf-8"))

jakeClient.close()