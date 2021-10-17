''' 
Inspired by the UDP section in the textbook - 2.7

/media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/Test_Files/UncensoredText/uncensored.txt
'''

import socket

jakeClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#---
# Getting File Path Location
pathName = input("List the path name for the import file WITHOUT QUOTES: ")
print(pathName)



# Imports data from file into a string
# from https://www.tutorialkart.com/python/python-read-file-as-string/
textToChange = open(pathName)
wholeFileToString = textToChange.read()
textToChange.close()
print(wholeFileToString)


# Finding Out what the censored phrase is from user & phrase length
# from https://www.geeksforgeeks.org/python-string-length-len/
censorPhrase = input("What phrase is classified: ") 
#lengthOfCensorPhrase = len(censorPhrase) 

# Finding out what the replacement character is
replaceChar = input("What do you want to replace it with: ")


# Sending text to server so it can be censored
# Can I send multiple strings to the server? Will it accept them?
jakeClientUDP.sendto(wholeFileToString.encode(),(socket.gethostname(), 12001))


jakeClientUDP.sendto(censorPhrase.encode(),(socket.gethostname(), 12001))


jakeClientUDP.sendto(replaceChar.encode(),(socket.gethostname(), 12001))



# Recieving censored text back & saving to file
censoredMessage, serverAddress = jakeClientUDP.recvfrom(2048)

# printing to standard out
# from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
with open('./UDP_Censored_Output/TopSecretUDP.txt', 'w') as f:
    print(censoredMessage, file=f)


print(censoredMessage.decode())





jakeClientUDP.close()

#---

