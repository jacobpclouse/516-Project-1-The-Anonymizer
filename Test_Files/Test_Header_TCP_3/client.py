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

putMarker = 0 
keywordMarker = 0
commandPut = 'put' 
commandKeyword = 'keyword'


while userCommand.lower() != 'quit':


# Problems:
# - I can't break out of the second while loop (with putmarker or keywordmarker)
# - I Don't recieve anything on the server side! (how do I keep it open? and get a custom number of queries?)
# - Do I need to have the accpt statement before the while loop?

# will loop until both have a value
     #while (putMarker == 0 or keywordMarker == 0) and userCommand != 'quit':

        userCommand = input("What is your command: ")
        print(f"User Command: {userCommand}")

        if len(userCommand) <= 2:
            # making sure that the user is giving us correct parameters
            # need to do more checks to confirm that following characters are valid
            print("you need to give a valid command")

        # Check for 'put' Command
        elif (userCommand[:3]).lower() == 'put':
            # ** I am slicing based on order
            # https://www.w3schools.com/python/ref_func_range.asp

            print("THIS IS A PUT")
            userFilePath = userCommand[4:]

            textToChange = open(userFilePath)
            wholeFileToString = textToChange.read()
            textToChange.close()

            userStringLength = f"Len: {str(len(wholeFileToString))}"


            # Creating combine string with command and message
            putMessage = "put " + wholeFileToString
            print(putMessage)

            # changing flag for putmarker (shows we have a putmarker)
            putMarker = 1

            

        # Check for 'key' Command
        elif (userCommand[:7]).lower() == 'keyword':
            keyTemp = userCommand[8:]
            print("THIS IS A KEYWORD")

            # Creating combine string with command and key
            keyMessage = "keyword " + keyTemp
            print(keyMessage)

            # changing flag for keywordMarker (shows we have a keywordMarker)
            keywordMarker = 1

print(keyMessage, putMessage)


jakeClient.send(putMessage.encode())
jakeClient.send(keyMessage.encode())

# NEED TO SORT THE ARRAY 
# need to clear markers after you send off the data!
putMarker = 0
keywordMarker = 0




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
