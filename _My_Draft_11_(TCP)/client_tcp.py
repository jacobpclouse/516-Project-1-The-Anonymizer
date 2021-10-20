# /media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/Test_Files/UncensoredText/uncensored.txt

# Socket stuff
import socket


SocketIP = socket.gethostname()
SocketPortNumber = 12002

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
jakeClient.connect((SocketIP, SocketPortNumber))
# ---

# Variables
userCommand = ''
userFilePath = ''

censorPhrase = ''
wholeFileToString = ''

commandToServer = ''
# ---

# Functions


def cleanUp(stringToWipe, stringToWipe2, stringToWipe3):
    stringToWipe = ''
    stringToWipe2 = ''
    stringToWipe3 = ''
    print(f"{stringToWipe, stringToWipe2, stringToWipe3} have been wiped")


def copyTextToStringVar(inputFilePath, outputString):
    # Imports data from file into a string
    # from https://www.tutorialkart.com/python/python-read-file-as-string/
    textToChange = open(inputFilePath)
    outputString = textToChange.read()
    textToChange.close()
    print(outputString)

# ---

# trying to make a while loop that I can use to input commands

# FOR TEXT: I am going to assume the the text file will be in the same directory as this file
# need to store information in array (command will always be command[0] position)

# need to make command lowercase THEN compair it to see if it is quit
# https://www.programiz.com/python-programming/methods/string/lower
while userCommand.lower() != 'quit':
    userCommand = input("What is your command: ")
    # splitting off 1st three bytes in order to compair
    userFirst3 = userCommand[0:3].lower()
    userRemainingCommand = userCommand[4:]

    if len(userCommand) <= 3:
        # making sure that the user is giving us correct parameters
        # need to do more checks to confirm that following characters are valid
        print("you need to give a valid command")

    # make sure that each of the target string, no no word and censored char are not empty

    # Check for 'put' Command
    # Upload Text file & send to server
    elif userFirst3 == 'put':
        # ** Can we assume that the file is in the same directory? Or in a predefined directory?
        # ** I am assuming that we only need 'put text.txt' and not 'put /main/docs/My Files/text.txt'
        # ** I am slicing based on order, can we expect other orders like text.txt put?
        # ** can we assume the order that the server is going to get this in?
        # https://www.w3schools.com/python/ref_func_range.asp

        userFilePath = userRemainingCommand
        copyTextToStringVar(userFilePath, wholeFileToString)
        print(f"String is: {wholeFileToString}")

        # Packaging up command
        commandToServer = userFirst3 + wholeFileToString

        # Sending command + data  to server
        jakeClient.send(commandToServer.encode())



        # cleaning up
        cleanUp(userCommand, userFirst3, userRemainingCommand)

    # Check for 'get' Command
    # Get censored text back from server
    elif userFirst3 == 'get':
        print(userRemainingCommand)


        # cleaning up
        cleanUp(userCommand, userFirst3, userRemainingCommand)

    # Check for 'keyword' command
    elif userFirst3 == 'key':
        censorPhrase = userCommand[8:]
        print(f"Keyword to replace: {censorPhrase}")

        # cleaning up
        cleanUp(userCommand, userFirst3, userRemainingCommand)

    # sending data to server
    # elif censorPhrase != '' and wholeFileToString != '':
    #     print()
