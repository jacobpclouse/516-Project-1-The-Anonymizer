# import sys

# def returnPort():
#     inputVar = int(sys.argv[1])
#     return inputVar
#     # Return Statement in function to return value
#     # https://www.w3schools.com/python/python_functions.asp

# myPort = returnPort()

# print(f"My Port number is: {myPort}")
# print(f"Type of myport: {type(myPort)}")


userInput = input("Give me 4 words with spaces")

userCommandArray = userInput.split(' ', 2)
print(f"User command: {userCommandArray}")