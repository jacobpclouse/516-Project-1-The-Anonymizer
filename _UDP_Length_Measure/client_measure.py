import socket

jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

needToGetLengthOf = input("Give me some text")
# getting length of Sting
# from https://www.geeksforgeeks.org/python-string-length-len/
actualLength = len(needToGetLengthOf)

# Sending
jakeClientUDP.sendto(actualLength.encode(),(socket.gethostname(), 12002))


# Recieving censored text back
serverLengthSentBack, serverAddress = jakeClientUDP.recvfrom(2048)

# Print out to check
print(f"The length of the text sent is {serverLengthSentBack}")