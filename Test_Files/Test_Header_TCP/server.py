import socket

# variables
keywordToCensor = ''
textToCensor = ''

SocketIP = socket.gethostname()
SocketPortNumber = int(input("Give me a port Number: "))

jakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
jakeServer.bind((SocketIP, SocketPortNumber))


# Functions


# shows server is up and running
print("The server is ready to receive")

# buffer set to 5
jakeServer.listen(5)


while True:
    clientSocket, clientAddress = jakeServer.accept()
    print(f"Connection from {clientAddress} has been established.")

    # do while other variables are empty

    incomingData = clientSocket.recv(2048).decode()
    print(f"Message 1 = {incomingData}")

    incomingData2 = clientSocket.recv(2048).decode()
    print(f"Message 2 = {incomingData2}")

    # need to clear both of these once data has been sent
    # otherwise, it will skip the while loop
    keywordToCensor = ''
    textToCensor = ''
    while textToCensor == '' and keywordToCensor == '':
    # -- Parsing what has been recieved
        # Incoming Data stream 1
        whatCommandIsIt = incomingData[:3]
        if whatCommandIsIt == 'put':
            textToCensor = incomingData[4:]
            print(textToCensor)

        elif whatCommandIsIt == 'key':
            keywordToCensor = incomingData[4:]
            print(keywordToCensor)


        # Incoming Data stream 2
        whatCommandIsIt = incomingData2[:3]
        if whatCommandIsIt == 'put':
            textToCensor = incomingData2[4:]
            print(textToCensor)

        elif whatCommandIsIt == 'key':
            keywordToCensor = incomingData2[4:]
            print(keywordToCensor)

        
        # Incoming Data stream 2
        # whatCommandIsIt = incomingData2[:3]
        # print(whatCommandIsIt)

        # if whatCommandIsIt == 'put':
        #     textToCensor = incomingData2[4:]
        #     print(textToCensor)

        # elif whatCommandIsIt == 'key':
        #     keywordToCensor = incomingData2[4:]
        #     print(keywordToCensor)

'''
        command1 = incomingData[:3]
        print(command1)

        datafromUser2 = incomingData[4:]
        print(datafromUser2)

        if command1 == 'put':
            textToCensor = incomingData[4:]
            print(textToCensor)

        elif command1 == 'key':
            keywordToCensor = incomingData[4:]
            print(keywordToCensor)
'''
