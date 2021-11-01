# put /media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/Test_Files/UncensoredText/uncensored.txt

# Socket stuff
import socket

SocketIP = socket.gethostname()
SocketPortNumber = int(input("Give me a port Number: "))

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeClient.connect((SocketIP, SocketPortNumber))


userCommand = ''

while userCommand.lower() != 'quit':

    userCommand = input("What is your command: ")
    print(f"User Command: {userCommand}")
