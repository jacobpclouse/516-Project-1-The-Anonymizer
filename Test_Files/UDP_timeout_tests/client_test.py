
# Import libraries
import socket
import sys

import time

# ---

# Functions:

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

#Setting up socket 
jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ---

# Variables
userCommand = ''
userCommandArray = ['', '']
lengthOfChunk = 1000
getLengthOfChunk = 1000
confirmationServerAck = ''




# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []
chunkBookmark = 0

# ---

# Main Logic!



sample1 = input("Enter Command: ")
# Sending length of file to server first
jakeClientUDP.sendto(sample1.encode(), (SocketIP, SocketPortNumber))


# from server
serverAck, clientAddress = jakeClientUDP.recvfrom(2048)
serverAck = serverAck.decode()
print(f"Message from server: {serverAck}")

time.sleep(2)
# second piece of data
sample2 = "Must be sent right away!"
jakeClientUDP.sendto(sample2.encode(), (SocketIP, SocketPortNumber))


#----
# end
jakeClientUDP.close()
