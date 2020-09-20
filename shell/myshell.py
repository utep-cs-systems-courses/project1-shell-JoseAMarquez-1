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
        elif "cd " in userInput:
            shell_cd(userInput)
        elif ">" or "<" in userInput:
            shell_fork(userInput)
        elif "|" in userInput:
            shell_pipie(userInput)
        else:
            shell_command(userInput)


if '__main__' == __name__:
    main()
