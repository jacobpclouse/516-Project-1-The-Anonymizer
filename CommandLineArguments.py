import sys

def returnPort():
    inputVar = int(sys.argv[1])
    return inputVar
    # Return Statement in function to return value
    # https://www.w3schools.com/python/python_functions.asp

myPort = returnPort()

print(f"My Port number is: {myPort}")
print(f"Type of myport: {type(myPort)}")