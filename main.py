# HIII
# Christopher Matheson

import os


def compress(file):
    pass


def decompress(file):
    pass


print(
    'Welcome to our very well coded and documented compression program! (Please note that this program is not well coded or documented)')
print('Would you like to compress or decompress a file? (c/d)', end='')
choice = input()

if choice == 'c':
    print('You have chosen to compress a file')
    print('Please enter the name of the file you would like to compress: (Same folder as py file)', end='')
    file_name = input()

elif choice == 'd':
    print('You have chosen to decompress a file')
    print('Please enter the name of the file you would like to decompress: (Same folder as py file)', end='')
    file_name = input()
    if not os.path.exists(file_name):
        print('File does not exist')
        exit()
    else:
        file = open(file_name, 'r')
        decompress(file)
