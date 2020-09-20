import os, sys, time, re

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
    os.write(1, "pipe".encode())
    pass

def shell_fork(userInput):
    os.write(1, "fork".encode())
    if '>' in userInput:
        pass
    elif "<" in userInput:
        pass

def shell_command(userInput):
    pid = os.getpid()
    rc = os.fork()

    if rc < 0:
        sys.exit(1)
    elif rc == 0:
        userInputList = userInput.split(" ")
        args = userInputList

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
