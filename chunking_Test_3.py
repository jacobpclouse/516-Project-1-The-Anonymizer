# abcdefghijklmnopqrstuvwxyz123456789



# creating array to append seperate strings to
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
arrayToSend = []

# Functions: 

def chunkerFunction(string):
    
    # Variables:

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

    # ---

    # Logic:

    # implimenting a sort of do while loop
    # https://www.educative.io/edpresso/how-to-emulate-a-do-while-loop-in-python
    while True:
        # printing out chunk equal to byte size
        print(string[startCut:endCut])
        arrayToSend.append(string[startCut:endCut])

        # Incrimenting startCut and endCut by byteSize
        startCut += byteSize
        endCut += byteSize

        # Decrimenting lengthLeft
        lengthLeft -= byteSize

        # If lengthLeft is less than or equal to byteSize, just print out what is left and end it
        if(lengthLeft <= byteSize):
            print(string[startCut:])
            arrayToSend.append(string[startCut:])
            break


message = input("Give us a string to break up: ")
chunkerFunction(message)

# Outputting variables in Array
print(f"The Array: {arrayToSend}")

# Outputting length of Array (ie: how many chunks to send)
# https://www.w3schools.com/python/gloss_python_array_length.asp
print(f"Array Length: {len(arrayToSend)}")


# Loop through Array:
for chunks in arrayToSend:
    print(f"Chunk {chunks}")

# need to figure out a way to let the server know how many chunks it can expect 
# also need to give it time to operate on those chunks, store them and then send the next chunk