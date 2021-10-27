''' 

STOP N WAIT
Inspired by the UDP section in the textbook - 2.7

'''


from os import replace
import socket
import sys



jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ---
# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []
chunkBookmark = 0

# Functions:

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


# ---

# Getting File Path Location
pathName = input("List the path name for the import file WITHOUT QUOTES: ")
print(pathName)


# Imports data from file into a string
# from https://www.tutorialkart.com/python/python-read-file-as-string/
textToChange = open(pathName)
wholeFileToString = textToChange.read()
textToChange.close()
#print(wholeFileToString)


# Finding Out what the censored phrase is from user & phrase length
# from https://www.geeksforgeeks.org/python-string-length-len/
censorPhrase = input("What phrase is classified: ")
#lengthOfCensorPhrase = len(censorPhrase)

# Finding out what the replacement character is
#replaceChar = input("What do you want to replace it with: ")
replaceChar = "X"
canContinue = True

while canContinue == True:
    # Sending text to server so it can be censored
    try: 
        jakeClientUDP.sendto(wholeFileToString.encode(), (SocketIP, SocketPortNumber))

        # timing out if response is not recieved after x seconds
        jakeClientUDP.settimeout(1)

        # Recieve Ack
        lenAck, serverAddress = jakeClientUDP.recvfrom(2048)
        lenAck = lenAck.decode("utf-8")
        print(f"Server ACK: {lenAck}")

    except:
        print("Connection Timed Out on String - Client Program")
        canContinue = False
        break

    # ----


    try: 
        # keyword sent
        jakeClientUDP.sendto(censorPhrase.encode(), (SocketIP, SocketPortNumber))

        # timing out if response is not recieved after x seconds
        jakeClientUDP.settimeout(1)

        # Recieve Ack
        lenAck, serverAddress = jakeClientUDP.recvfrom(2048)
        lenAck = lenAck.decode("utf-8")
        print(f"Server ACK: {lenAck}")

    except:
        print("Connection Timed Out on Keyword - Client Program")
        canContinue = False
        break

    # ----

    try:
        # replacement char sent
        jakeClientUDP.sendto(replaceChar.encode(), (SocketIP, SocketPortNumber))

        # timing out if response is not recieved after x seconds
        jakeClientUDP.settimeout(1)

        # Recieve Ack
        lenAck, serverAddress = jakeClientUDP.recvfrom(2048)
        lenAck = lenAck.decode("utf-8")
        print(f"Server ACK: {lenAck}")

    except:
        print("Connection Timed Out on Replacement Char - Client Program")
        canContinue = False
        break


    try:
        # Recieving censored text back & saving to file
        censoredMessage, serverAddress = jakeClientUDP.recvfrom(2048)
        censoredMessage = censoredMessage.decode("utf-8")

        # timing out if response is not recieved after x seconds
        jakeClientUDP.settimeout(10)

        # printing to standard out
        # from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
        with open(f'./UDP_Censored_Output/Censored_{pathName}', 'w') as f:
            print(censoredMessage, file=f)
    
    except:
        print("Error Encountered When Recieving Censored output")
        canContinue = False
        break


    canContinue = False

    jakeClientUDP.close()

    # ---