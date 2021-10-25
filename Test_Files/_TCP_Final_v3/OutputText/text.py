serverCensoredName = 'anonText.txt'
FillerText = "This text should be inside the text of anonText"

f = open(f"{serverCensoredName}", "x")

with open(f"{serverCensoredName}", 'w') as f:
    print(FillerText, file=f)

