#! /usr/bin/env python3

import os, sys, time, re

running_state = 1
shell = '$'

#will running_state = 1 run else terminate
while running_state:
    os.write(1, (shell).encode())

    userInput = input()
    userInput = userInput.split(" ")

    #if exit change running state to 0 (while loop terminated)
    if userInput[0] == 'exit' :
        os.write(1, ("The System cannot find the path specidied ").encode())
        running_state = 0
        exit()

    elif userInput[0] == 'cd':
        if len(userInput) > 2:
            os.write(1, ("The System cannot find the path specidied ").encode())
            pass
        else:
            newDir = userInput[1]
            os.write(1,(newDir).encode())
        try:
            os.chdir(newDir)
            os.write(1, (os.getcwd()).encode())
        except FileNotFoundError:
            os.write(1, ("The System cannot find the path specidied \n").encode())
            pass
        continue
