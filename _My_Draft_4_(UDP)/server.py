''' 
Inspired by the UDP section in the textbook - 2.7

Could I possibly just append the top secret phrase and secret character to the end of the 
full string and then remove them later? Get length of string before and after and add that as well?

2) how can we set is so that the server knows to move along?
'''

import socket


jakeServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
jakeServerUDP.bind((socket.gethostname(), 12001))

# Server prints this if it has been successfully created 
print('The server is ready to receive')

while True:
    #Recieving uncensored text string from client
    uncensoredText, clientAddress = jakeServerUDP.recvfrom(2048)

    #Putting uncensored text into modified variable
    serverNeedToCensor = uncensoredText.decode()

#--

    #Recieving Top Secret phrase from client
    topSecretPhrase, clientAddress = jakeServerUDP.recvfrom(2048)

    #Putting Top Secret phrase into modified variable
    serverSecretPhrase = topSecretPhrase.decode()

#--

    #Recieving replacement character from client
    replacementChar, clientAddress = jakeServerUDP.recvfrom(2048)

    #Putting replacement character into modified variable
    serverReplacementChar = replacementChar.decode()

#--


    # Discovering the length of the Top secret phrase
    lengthOfCensorPhrase = len(serverNeedToCensor)

    print(f"RECIEVED {serverSecretPhrase, serverNeedToCensor, serverReplacementChar} FROM {clientAddress}")


    jakeServerUDP.sendto(serverSecretPhrase.encode(), clientAddress)