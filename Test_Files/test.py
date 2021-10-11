#! /usr/bin/python
''' This is working through python videos from the playlist: 

https://www.youtube.com/watch?v=B7G5B8P8k9s&list=PL98qAXLA6afuh50qD2MdAj3ofYjZR_Phn&index=1

Questions:
1) For automated testing, how do we know where the file is going to be stored? Do we have to 
hard code in the path name in order to import the text? Or should the user be able to enter that?
'''

# from https://www.tutorialkart.com/python/python-read-file-as-string/
textToChange = open("/media/jake/WDC 500GB/How to learn anything")
wholeFileToString = textToChange.read()
textToChange.close()
print(wholeFileToString)



censorPhrase = input("What phrase is classified?") #need to have a function that finds the length of this character
lengthOfCensorPhrase = len(censorPhrase) # from https://www.geeksforgeeks.org/python-string-length-len/
replaceChar = input("What do you want to replace it with?")


#Gets length of string and creates the character to replace it with
replacementString = ''

for letters in censorPhrase:
    replacementString += replaceChar

print(replacementString)



# from https://www.geeksforgeeks.org/python-string-replace/
censoredOutput = wholeFileToString.replace(censorPhrase, replacementString)
print(censoredOutput)