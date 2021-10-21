"""
You can re-run the client to re-execute the program
Send data as soon as you get it (ie: get a put, then send it off right away, don't wait and lump together)

You don't need to keep track of state for TCP
You can assume that the file will be in the same directory as the program
You can use main function and pass in port number as an argument
You can assume that put comes first, then keyword, then get (can throw an error if empty)
KEYWORD command only gives you the keyword to censor and points to the filename to censor it on
ACK command will be impliment like you previously tried to impliment PUT command (ie: with STATE)
Don't overwrite your files! put them in seperate directories!
Don't worry about sequence numbers and duplicates for your UDP implimentation
You can have x2 receivers on the server side, just needs program to repeat!
If the user makes a mistake (ie: gives wrong keyword) that on them (don't worry about giving them another shot)

** THINK about HOW you are going to impliment string splitting!
"""


# put /media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/Test_Files/UncensoredText/uncensored.txt
# put /media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/_TCP_Final/uncensored_text.txt
# put uncensored_text.txt


# Socket stuff
import socket


SocketIP = socket.gethostname()
SocketPortNumber = int(input("Give me a port Number: "))

jakeClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
jakeClient.connect((SocketIP, SocketPortNumber))
# ---

# Variables
userCommand = ''

# ---

# Functions

# ---

# Main Logic!
    # try breaking this out into its own function if it works (then can call it)
    # ** Might try having the entire function under this command if it works (empty string)
while userCommand == '':
    userCommand = input("Waiting for command: ")

    if userCommand.lower() == 'quit':
        break

    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    # ** break out into function
userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")


# 'put' Command
# opening file
#userFilePath = userCommandArray[1]
#textToChange = open(userFilePath)
textToChange = open(userCommandArray[1])
wholeFileToString = textToChange.read()
textToChange.close()

print(wholeFileToString)

# sending put string to server
# assuming first string is always 'put'
jakeClient.send(wholeFileToString.encode())


userCommand = ''


# ---


    # prompting user for next command
while userCommand == '':
    userCommand = input("Waiting for command: ")

    if userCommand.lower() == 'quit':
        break

    # Split on String
    # https://www.tutorialspoint.com/python/string_split.htm
    # ** break out into function
userCommandArray = userCommand.split(' ', 1)
print(f"User command: {userCommandArray[0]}")


# -- 

# 'keyword' command
# specifies phrase to censor AND file to censor the word in
userCensorPhraseNFile = userCommandArray[1]

print(userCensorPhraseNFile)

# sending keyword phrase and filename to operate on to server
# assuming second string is always 'keyword'
jakeClient.send(userCensorPhraseNFile.encode())

userCommand = ''








# can use another split on this to seperate out the keyword from the filename (only one split!)
# elif userCommandArray[1] == 'keyword':
#     print("This command is a KEY!")

#     print(userCommandArray[1])


# trying to make a while loop that I can use to input commands
# https://www.programiz.com/python-programming/methods/string/lower
# while userCommand.lower() != 'quit':
#     userCommand = input("What is your command: ")

#     # splitting off 1st three bytes in order to compair
#     userFirst3 = userCommand[0:3].lower()
#     userRemainingCommand = userCommand[4:]

#     if len(userCommand) <= 3:
#         # making sure that the user is giving us correct parameters
#         # need to do more checks to confirm that following characters are valid
#         print("you need to give a valid command")

#     # make sure that each of the target string, no no word and censored char are not empty

#     # Check for 'put' Command
#     # Upload Text file & send to server
#     elif userFirst3 == 'put':
#         # ** Can we assume that the file is in the same directory? Or in a predefined directory?
#         # ** I am assuming that we only need 'put text.txt' and not 'put /main/docs/My Files/text.txt'
#         # ** I am slicing based on order, can we expect other orders like text.txt put?
#         # ** can we assume the order that the server is going to get this in?
#         # https://www.w3schools.com/python/ref_func_range.asp

#         userFilePath = userRemainingCommand
#         textToChange = open(userFilePath)
#         wholeFileToString = textToChange.read()
#         textToChange.close()
# userCommand

#         # Sending string to censor to server
#         print('Sending out String Data')
#         jakeClient.send(wholeFileToString.encode())

#         # calculating, converting to str, and sending length
#         userDataLength = str(len(wholeFileToString))
#         jakeClient.send(userDataLength.encode())

#     # Check for 'get' Command
#     # Get censored text back from server
#     elif userFirst3 == 'get':
#         print(userRemainingCommand)


#     # Check for 'keyword' command
#     elif userFirst3 == 'key':
#         censorPhrase = userCommand[8:]
#         print(f"Keyword to replace: {censorPhrase}")


#     # Sending string to censor to server
#     jakeClient.send(censorPhrase.encode())
