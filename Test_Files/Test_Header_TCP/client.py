# Socket stuff
import socket



SocketIP = socket.gethostname()
SocketPortNumber = int(input("Give me a port Number: "))

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
jakeClient.connect((SocketIP, SocketPortNumber))


# Variables
putMessage = ''
keyMessage = ''
command = ''

while putMessage == '' or keyMessage == '':
    #while command != 'put' or command != 'key':
    command = input("put, get or key?: ")

    msg2 = input("Give me a phrase: ")

    if command.lower() == 'put':
        putMessage = command.lower() + " " + msg2
        print(putMessage)

    elif command.lower() == 'key':
        keyMessage = command.lower() + " " + msg2
        print(keyMessage)


jakeClient.send(putMessage.encode())
jakeClient.send(keyMessage.encode())

    # jam it both files together, read the first 3 as the header of sorts, then read the rest from the file