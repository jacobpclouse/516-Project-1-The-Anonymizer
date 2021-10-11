#! /usr/bin/python
''' This is working through python videos from the playlist: 

/media/jake/WDC 500GB/HOW TO STUDY

https://www.youtube.com/watch?v=B7G5B8P8k9s&list=PL98qAXLA6afuh50qD2MdAj3ofYjZR_Phn&index=1

Questions:
1) For automated testing, how do we know where the file is going to be stored? Do we have to 
    hard code in the path name in order to import the text? Or should the user be able to enter that?

2) Do we need to have any checks on the file to make sure that it is a valid text file? 
    What kind of checks would be sufficient? (ie: just check that it has a .txt ending?)
    Do we need to limit the file size? (ie: if a text is above the file limit, it won't accept it?)

3) For this example, i have been using a single character (ie: 'x') and then repeating it for how long
    the target word is (ie: read would be xxxx). Will we have to cover phrases? (ie: use 'TEST' and 
    cut it/repeat it for how long a word would be? Ex: Universitiy would be TESTTESTTES)

4) Do output files need to be directed to a specific directory?

5) How do we print text to a file WITHOUT using 'sys'?
    Is there any way that we could include it in the imported libraries?

6) Do we have to create our own checksum from scratch? (for UDP)

7) Will the list of phrases to find/replace be standard for all students?
    Will we need to impliment a catch in case the word doesn't exist in the file?

8) Is it alright if my program overrides the previous output in the file?

9) Do we have to be able to censor multiple words?
'''
# We can't use libraries, but 'sys' is used to print text to a file
import sys


# allowing the user to designate path name:
pathName = input("List the path name for the import file WITHOUT QUOTES")
print(pathName)


# Imports data from file into a string
# from https://www.tutorialkart.com/python/python-read-file-as-string/
textToChange = open(pathName)
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



# Doing find and replace
# from https://www.geeksforgeeks.org/python-string-replace/
censoredOutput = wholeFileToString.replace(censorPhrase, replacementString)
print(censoredOutput)



# printing to standard out
# from https://stackabuse.com/writing-to-a-file-with-pythons-print-function/
with open('./OutputFiles/TopSecretOutput.txt', 'w') as f:
    print(censoredOutput, file=f)