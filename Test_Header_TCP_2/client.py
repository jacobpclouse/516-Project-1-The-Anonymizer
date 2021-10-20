# put /media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/Test_Files/UncensoredText/uncensored.txt


# Socket stuff
import socket

SocketIP = socket.gethostname()
SocketPortNumber = int(input("Give me a port Number: "))

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeClient.connect((SocketIP, SocketPortNumber))

# -- FROM COMMAND LOOP
userCommand = ''
userFilePath = ''
userKeywordToCensor = ''
userStringLength = ''

putMessage = ''
keyMessage = ''


while userCommand.lower() != 'quit':
    # will loop until both have a value
    #while putMessage == '' or keyMessage == '':
        
        userCommand = input("What is your command: ")

        userFirst3 = userCommand[0:3].lower()
        userRemainingCommand = userCommand[4:]



        if len(userCommand) <= 3:
            # making sure that the user is giving us correct parameters
            # need to do more checks to confirm that following characters are valid 
            print("you need to give a valid command")

        # Check for 'put' Command
        elif userFirst3 == 'put':
            # ** I am slicing based on order
            # https://www.w3schools.com/python/ref_func_range.asp
            userFilePath = userRemainingCommand

            textToChange = open(userFilePath)
            wholeFileToString = textToChange.read()
            textToChange.close()

            userStringLength = str(len(wholeFileToString))
            putMessage = userFirst3 + " " + wholeFileToString
            
            print(putMessage)

            print("Sending Put Message:")
            jakeClient.send(putMessage.encode())

        # Check for 'key' Command
        elif userFirst3 == 'key':
            keyMessage = userCommand
            print(keyMessage)

            print("Sending Key Message:")
            jakeClient.send(keyMessage.encode())




# -- ORIGINAL CODE
# Variables
# putMessage = ''
# keyMessage = ''
# command = ''

# while putMessage == '' or keyMessage == '':
#     #while command != 'put' or command != 'key':
#     command = input("put, get or key?: ")

#     msg2 = input("Give me a phrase: ")

#     if command.lower() == 'put':
#         putMessage = command.lower() + " " + msg2
#         print(putMessage)

#     elif command.lower() == 'key':
#         keyMessage = command.lower() + " " + msg2
#         print(keyMessage)


# jakeClient.send(putMessage.encode())
# jakeClient.send(keyMessage.encode())

    # jam it both files together, read the first 3 as the header of sorts, then read the rest from the file