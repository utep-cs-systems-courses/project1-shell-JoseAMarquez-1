import os, sys, time, re
from shellmethods import *

state = True
PS1 = '$'

def main():
    global state
    while state:
        os.write(1, (PS1).encode())
        userInput = input()
        userInputList = userInput.split(" ")

        if userInputList[0] == "exit":
            state = False
        elif "cd" in userInputList:
            shell_cd(userInput)
        elif '>' in userInputList:
            shell_fork(userInput)
        elif '<' in userInputList:
            shell_fork(userInput)
        elif '|' in userInputList:
            shell_pipie(userInput)
        else:
            shell_command(userInput)


if '__main__' == __name__:
    main()
