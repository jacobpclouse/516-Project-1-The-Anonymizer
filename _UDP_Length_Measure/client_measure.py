import socket

jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

needToGetLengthOf = input("Give me some text: ")
# getting length of Sting
# from https://www.geeksforgeeks.org/python-string-length-len/
actualLength = str(len(needToGetLengthOf))

# Sending
jakeClientUDP.sendto(actualLength.encode(),(socket.gethostname(), 12002))


# Recieving censored text back
# In order to use this, it has to be converted from str to int
serverLengthSentBack, serverAddress = jakeClientUDP.recvfrom(2048)

# Saving server message length to variable
clientRecievedMessage = serverLengthSentBack.decode()

# Print out to check (converts to int as well)
print(f"The length of the text sent is {int(clientRecievedMessage)}")