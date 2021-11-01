command = 'noquit'
commandArray = ['', '', '']

while commandArray[0].lower() != 'quit':
    command = input("Give me a value: ")

    commandArray = command.split(' ', 1)
    print(f"User command: {commandArray[0]}")
    print(f"You gave me {commandArray}")




# I think its because i use a string an array, need to check the first letters the string

# counter = 0


# while True:
#     love = input("Give me a value: ")

#     if love.lower() == 'love':
#         print("Secret Code Accepted: Quitting...")
#         break

#     else:
#         print(love)
