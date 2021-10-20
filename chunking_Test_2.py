def chunkerFunction(string):
    # getting length of string
    stringLength = len(string)
    print(f"Length of String: {stringLength} characters")

    # determining the target size (ie: this will be 1000 for udp)
    byteSize = 10

    # setting a counter equal to length, will decriment as chunks are written
    lengthLeft = stringLength

    # setting start position variable, will incriment up
    startCut = 0

    # setting end cut (exclusive), will incriment up
    endCut = startCut + byteSize

    # seeing if the string is divided evenly by the remainder
    # remainder = stringLength % byteSize
    # dividesInto = stringLength / byteSize

# idea! def function(importvariable, export variable/array)
    # export variable = import variable ++


    # implimenting a sort of do while loop
    # https://www.educative.io/edpresso/how-to-emulate-a-do-while-loop-in-python
    while True:
        # printing out chunk equal to byte size
        print(string[startCut:endCut])

        # Incrimenting startCut and endCut by byteSize
        startCut += byteSize
        endCut += byteSize

        # Decrimenting lengthLeft
        lengthLeft -= byteSize

        # If lengthLeft is less than or equal to byteSize, just print out what is left and end it
        if(lengthLeft <= byteSize):
            print(string[startCut:])
            break




'''
 if lengthLeft <= byteSize:
        prin


# ---

    if remainder == 0:
        print("no remainder")
        print(f"length: {stringLength} Evenly dives into {dividesInto} times")

        
    else:
        print(f"THERE IS {remainder} REMAINDER in string")
        print(f"length: {stringLength} it Divides into it {dividesInto} times")
'''


message = input("Give us a string to break up: ")
chunkerFunction(message)


# first10 = message[:10]
# second10 = message[10:20]
# lastChar = message[20:]

# print(f"The first string is {first10} and is {len(first10)} long")
# print(f"The first string is {second10} and is {len(second10)} long")
# print(f"The first string is {lastChar} and is {len(lastChar)} long")

# Try and set the the send message into the function