'''
You don't have to use one overarching while loop!
or at least have on overarching one (with accept outside) that counts to stop too many loops
Then have nested while loops where you do stuff over an over again until you get the data you need
'''

import socket

# variables
keywordToCensor = ''
textToCensor = ''

counter = 0
totalLoopCycle = 0

piecesOfData = []

SocketIP = socket.gethostname()
SocketPortNumber = int(input("Give me a port Number: "))

jakeServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
jakeServer.bind((SocketIP, SocketPortNumber))


# Functions


# shows server is up and running
print("The server is ready to receive")

# buffer set to 5
jakeServer.listen(5)


# HOW DO I MAKE IT SO THAT I Can have unlimited recieves
# this only takes two before it konks out!
# I don't know how much data this is going to recieve, how do we do this?
# can i use an array?

# Moved 'clientSocket, clientAddress = jakeServer.accept()' outside the array and it keeps going through
clientSocket, clientAddress = jakeServer.accept()
#while True:
while totalLoopCycle <= 50:
    #clientSocket, clientAddress = jakeServer.accept()
    print(f"Connection from {clientAddress} has been established.")

    counter = 0 # change to length of incoming, need to get length first
    while (counter < 4):
        piecesOfData.append(clientSocket.recv(2048).decode())
        print(piecesOfData)
        counter +=1
        print(counter)

    print ("broken out of loop")
    # break up the keyword from the statement, put in seperate parts of array!
    print (piecesOfData[0])


    #Total loop cycles 
    totalLoopCycle += 1
'''    
    # get length then do for loop up to length?
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

    print("Done with while loop!")
'''