''' 
Sample path:
PUt/media/jake/WDC 500GB/ICSI 516/Project 1/Code Project 1/client server draft 1/Test_Files/UncensoredText/uncensored.txt
'''

# trying to make a while loop that I can use to input commands
userCommand = ''
userFilePath = ''
userKeywordToCensor = ''

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
    
    # Check for 'put' Command
    elif userFirst3 == 'put':
        # ** Can we assume that the file is in the same directory? Or in a predefined directory?
        # ** I am assuming that we only need 'put text.txt' and not 'put /main/docs/My Files/text.txt'
        # ** I am slicing based on order, can we expect other orders like text.txt put?
        # https://www.w3schools.com/python/ref_func_range.asp
        userFilePath = userRemainingCommand
        # cleaning up
        userCommand = ''

    # Check for 'get' Command
    elif userFirst3 == 'get':
        #
        print(userRemainingCommand)
        # cleaning up
        userCommand = ''
