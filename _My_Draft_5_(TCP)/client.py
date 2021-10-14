'''
This was inspired by https://pythonprogramming.net/sockets-tutorial-python-3/ 

/media/jake/WDC 500GB/_Downloads/Downloads/SCP-6668

/media/jake/WDC 500GB/HOW TO STUDY

/media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/Test_Files/UncensoredText/uncensored.txt
'''

import socket

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
jakeClient.connect((socket.gethostname(), 12000))

#---
# allowing the user to designate path name:
pathName = input("List the path name for the import file (WITHOUT QUOTES): ")
print(pathName)


# Imports data from file into a string (DOES THIS NEED TO BE DONE ON THE SERVER SIDE?)
# from https://www.tutorialkart.com/python/python-read-file-as-string/
textToChange = open(pathName)
wholeFileToString = textToChange.read()
textToChange.close()
print(wholeFileToString)


# Finding out the Top Secret Word
censorPhrase = input("What phrase is classified: ")

# Getting length of Top Secret Word
# from https://www.geeksforgeeks.org/python-string-length-len/
#lengthOfCensorPhrase = len(censorPhrase)

# Designating the replacement character (ie: 'X')
replaceChar = input("What do you want to replace it with: ")


# Send out text to censtor to server
jakeClient.send(wholeFileToString.encode())


# Send out the Top Secret Word to server
jakeClient.send(censorPhrase.encode())


# Send out the replacement character to server
jakeClient.send(replaceChar.encode())


# Getting censored message back from server & printing out
censoredMessage = jakeClient.recv(2048)
print(f'From Server: {censoredMessage.decode()}')


#Do I need to print the output to a file on the server side or on the client side?
#ie: am I just sending a sting back or an entire file?

#---

# printing to standard out
# from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
with open('./TCP_Censored_Output/TopSecretTCP.txt', 'w') as f:
    print(censoredMessage, file=f)


jakeClient.close()

