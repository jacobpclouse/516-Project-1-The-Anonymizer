def chunkerFunction(string):
    # getting length of string
    stringLength = len(string)
    # determining the target size
    byteSize = 10

    #seeing if the string is divided evenly by the remainder
    remainder = stringLength % byteSize
    dividesInto = stringLength / byteSize

# idea! def function(importvariable, export variable/array)
    # export variable = import variable ++

    if remainder == 0:
        print("no remainder")
        print(f"length: {stringLength} Evenly dives into {dividesInto} times")

        
    else:
        print(f"THERE IS {remainder} REMAINDER in string")
        print(f"length: {stringLength} it Divides into it {dividesInto} times")



message = input("Give us a string to break up: ")
chunkerFunction(message)


# first10 = message[:10]
# second10 = message[10:20]
# lastChar = message[20:]

# print(f"The first string is {first10} and is {len(first10)} long")
# print(f"The first string is {second10} and is {len(second10)} long")
# print(f"The first string is {lastChar} and is {len(lastChar)} long")


'''
# This works to break up a string of fixed length
message = input("Give us a string to break up: ")

first10 = message[:10]
second10 = message[10:20]
lastChar = message[20:]

print(f"The first string is {first10} and is {len(first10)} long")
print(f"The first string is {second10} and is {len(second10)} long")
print(f"The first string is {lastChar} and is {len(lastChar)} long")

#---

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


ListToChunk = input("Give me some text to chunk")

AfterChunking = chunks(ListToChunk, 5)

print(AfterChunking)

# ---

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

ListToChunk = input("Give me some text to chunk")

AfterChunking = chunks(ListToChunk, 5)

print(AfterChunking)'''


'''
Need to get length of string to send
need to see how many times that goes into 1000 bytes
need to impliment a program that will cut it up into 1000 byte segments evenly
need to have it select the remaining part of the list at the end.

could we cut it up beforehand and then have it put back together at the other end?
Maybe send and object with each segment?
'''