#! /usr/bin/env python3
import os, sys, time, re

def shell_cd(userInput):
    userInputList = userInput.split(" ")
    newDir = userInputList[1]
    try:
      os.chdir(newDir)
      os.write(1, (os.getcwd()).encode())
    except FileNotFoundError:
      os.write(1, ("The System cannot find the path specidied \n").encode())


def shell_pipie(userInput):
    pid  = os.getpid()
    pr, pw = os.pipe()

    for f in (pr,pw):
        os.set_inheritable(f,True)

    rc = os.fork()

    if rc < 0:
        print("fork failed, returning %d\n" % rc, file=sys.stderr)
        pass

    elif rc == 0:
        userInputList = userInput.split(" ")
        args = userInputList
        os.close(1)
        os.dup(pr,pw)
        os.set_inheritable(1, True)

        for fd in (pr,pw):
            os.close(fd)
        newProcess(userInput[0])
    else:
        os.close(0)
        os.dup(pr)
        for fd in (pw, pr):
            os.close(fd)
        newProcess(userInputList[2])

def shell_fork(userInput):
    os.write(1, "fork".encode())
    if '>' in userInput:
        pid = os.getpid()
        rc = os.fork()

        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            userInputList = userInput.split(" ")
            args = userInputList
            os.close(1)
            os.open(args[2], os.O_CREAT | os.WRONLY);
            os.set_inheritable(1,True)

            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program,args, os.environ)
                except FileNotFoundError:
                    pass
            sys.exit(1)
        else:
            childPidCode = os.wait()
            os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
             childPidCode).encode())

    elif "<" in userInput:
        pid = os.getpid()
        rc = os.fork()

        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            userInputList = userInput.split(" ")
            args = userInputList
            os.close(1) # output stdout
            os.open(args[args.index('>') +1], os,O_CREAT | os.O_WRONLY)
            os.set_inheritable(1,True)

            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program,args, os.environ)
                except FileNotFoundError:
                    pass
            sys.exit(1)
        else:
            childPidCode = os.wait()
            os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
             childPidCode).encode())

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
