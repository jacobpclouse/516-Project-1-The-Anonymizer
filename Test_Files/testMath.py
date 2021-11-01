# the rain in spain falls neatly in the drain

wholeFileToStringLength = input("Give me a string to work on: ")
fileLengthVar = len(wholeFileToStringLength)
print(f"Number of bytes: {fileLengthVar}")


# find out how many chunks of 1000 you will send, ceiling it
# https://www.geeksforgeeks.org/floor-ceil-function-python/
lengthOfChunk = 10
loopsOfChunk = fileLengthVar / lengthOfChunk
loopsOfChunkTrunk = int(loopsOfChunk)
print(loopsOfChunk)
print(loopsOfChunkTrunk)

#if original value and truncated value are not the same, we will increase truncated value by 1
if loopsOfChunk != loopsOfChunkTrunk:
    loopsOfChunk = loopsOfChunkTrunk + 1
    # this will be how many loops we will have to send
print(f"Expect {loopsOfChunk} loops")

# ----
# Chunk String
# ----
# append info to array
# https://www.freecodecamp.org/news/python-list-append-how-to-add-an-element-to-an-array-explained-with-examples/
user1000ByteArray = []

chunks = 0
starterPoint = 0
while chunks < loopsOfChunk:
    
    endPoint = starterPoint + lengthOfChunk
    # appending
    user1000ByteArray.append(wholeFileToStringLength[starterPoint:endPoint])

    print(f"On chunk: {chunks}, String to append is: {wholeFileToStringLength[starterPoint:endPoint]}")
    print("Array currently is:")
    print(user1000ByteArray)

    starterPoint = endPoint
    chunks += 1







# mathVar = float(input("Give me a number bigger than 1000"))

# math1 = mathVar / 1000
# math2 = int(math1)


# if (math1 != math2):
#     print("Values do not divide evenly")
# else:
#     print("Values divide evenly")