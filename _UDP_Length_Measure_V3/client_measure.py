import socket


# --
# Functions
# Help from: https://www.w3schools.com/python/python_functions.asp

# checks cliented reported measurement against actual length
# Might want to impliment a do while loop to query the client if the length is not correct


def checklength(ReportedLength, ActualLength):
    if (ReportedLength) == len(ActualLength):
        print("Lengths match")
        print(f"Message: {ActualLength}")
    else:
        print("LENGTHS DO NOT MATCH")
    # Might have to use a "Do/While Loop to keep querying for resend if message corrupted"


# --
# Defining variables (will be input by user in future)
portNum = 12002
socketNum = socket.gethostname()

#--
jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

needToGetLengthOf = input("Give me some text: ")
# getting length of Sting
# from https://www.geeksforgeeks.org/python-string-length-len/
actualLength = str(len(needToGetLengthOf))
print(f"The length of the message is: {actualLength}")
print(f"The message to be sent is: {needToGetLengthOf}")


# Sending Length
# jakeClientUDP.sendto(actualLength.encode(),(socket.gethostname(), 12002))
jakeClientUDP.sendto(actualLength.encode(),(socketNum, portNum))



# Sending actual text
#jakeClientUDP.sendto(needToGetLengthOf.encode(),(socket.gethostname(), 12002))
jakeClientUDP.sendto(needToGetLengthOf.encode(),(socketNum, portNum))

# --


# Recieving length of message to client
# In order to use this, it has to be converted from str to int
serverLengthSentBack, serverAddress = jakeClientUDP.recvfrom(2048)

# Saving server message length to variable
# In order to use this, will need to convert from string to int
clientRecievedLength = int(serverLengthSentBack.decode())


# --


# Recieving new message to client
serverMessageSentBack, serverAddress = jakeClientUDP.recvfrom(2048)

# Saving server message length to variable
clientRecievedMessage = serverMessageSentBack.decode()

# --

checklength(clientRecievedLength, clientRecievedMessage)


# --

# Print out to check (converts to int as well)
print(f"The text recieved is: {clientRecievedLength}")
print(f"The length recieved is: {clientRecievedMessage}")