# Getting bytes and delay from user
bytesInput = input("Give me total number of bytes: ")
delayInput = input("Give me delay in seconds: ")

# Need to multply x8 in order to git bits
bitsTotal = int(bytesInput) * 8

# throughput = L/R
throughput = bitsTotal / float(delayInput)

# printing
print(f"Throughput equals: {throughput} bps")