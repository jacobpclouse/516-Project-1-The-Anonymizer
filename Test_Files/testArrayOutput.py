user1000ByteArray = ["One", "Two", "Three", "Four", "Five"]
loopsOfChunk = 5
    
currentChunkIndex = 0

while currentChunkIndex < loopsOfChunk:
    print(f"On Array Section {currentChunkIndex}")


    #Sending to server
    outboundString = str(user1000ByteArray[currentChunkIndex])
    print(outboundString)
    

    # incriment
    currentChunkIndex += 1