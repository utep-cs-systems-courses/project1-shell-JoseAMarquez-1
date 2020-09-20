import os, sys, time, re, subprocess

def shell_cd(userInput):
    userInputList = userInput.split(" ")
    newDir = userInputList[1]
    os.write(1,(newDir).encode())
    try:
      os.chdir(newDir)
      os.write(1, (os.getcwd()).encode())
    except FileNotFoundError:
      os.write(1, ("The System cannot find the path specidied \n").encode())


def shell_pipie(userInput):
    pass

def shell_fork(userInput):
    if '>' in userInput:
        pass
    elif "<" in userInput:
        pass

def shell_command(userInput):
    pid = os.getpid()
    rc = os.fork()

    if rc < 0:
        sys.exit(1)
    elif r == 0:
        userInputList = userInput.split(" ")
        args = [userInputList[0],userInputList[1]]

        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass

        os.write(2, ("Could not exec %s\n" % args[0]).encode())
        sys.exit(1)

    else:
        childPidCode = os.wait()
