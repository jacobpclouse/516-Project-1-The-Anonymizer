# THIS USES PYTHON Python 3.8.10

'''
 This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 
 
 Questions: 


15) where do i put timeouts?!?****8

 '''

# -----------------------------------
# -----------------------------------

# Import libraries
import socket
import sys


# --
# Functions

# Gets length of string and creates the character to replace it with
def myFindTargetString(targetPhase):
    replacementString = ''
    replacementChar = 'X'
    for letters in targetPhase:
        replacementString += replacementChar
    return replacementString



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



# Main Logic
# ---

jakeServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
jakeServerUDP.bind((SocketIP, SocketPortNumber))



# --


# Variables

isTimeout = False


# added



# ---
# Program logic
# ---


# shows server is up and running
print("Server Is Online")


# going to get data from client, loop until manually stoped
while True:
    # Server prints this if it has been successfully created
    print(f'The server is ready to receive on Hostname: {SocketIP}, Port: {SocketPortNumber}')

    incomingTest1, clientAddress = jakeServerUDP.recvfrom(2048)
    incomingTest1 = incomingTest1.decode()

    print(incomingTest1)

    testAck = 'Server recieved data'
    jakeServerUDP.sendto(testAck.encode(), clientAddress)


    # next string of incoming data, must be recieved within 1 sec of prevous data
    jakeServerUDP.settimeout(1)
    try:
        incomingTest2, clientAddress = jakeServerUDP.recvfrom(2048)
        incomingTest2 = incomingTest2.decode("utf-8")

        print(incomingTest2)
    except:
        print("Data Took too long")
        isTimeout = True
        

    jakeServerUDP.settimeout(None)

    if isTimeout == False:
        print("You shouldn't see this after a timeout")
   
