#! /usr/bin/env python3

import os, sys, time, re


def newProcess(args):
    pid = os.getpid()
    rc = os.fork()

    if rc < 0:
        sys.exit(1)

    elif rc == 0:
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


running_state = 1
shell = '$'

#will running_state = 1 run else terminate
while running_state:
    os.write(1, (shell).encode())

    userInput = input()
    userInputList = userInput.split(" ")



    #if exit change running state to 0 (while loop terminated)
    if userInputList[0] == 'exit' :
        os.write(1, ("Exiting Shell...").encode())
        running_state = 0
        exit()

    elif userInputList[0] == 'cd':
        if len(userInputList) > 2:
            os.write(1, ("The System cannot find the path specidied ").encode())
            pass
        else:
            newDir = userInputList[1]
            os.write(1,(newDir).encode())
        try:
            os.chdir(newDir)
            os.write(1, (os.getcwd()).encode())
        except FileNotFoundError:
            os.write(1, ("The System cannot find the path specidied \n").encode())
            pass
        continue

    elif '>' in userInputList:
        if len(userInputList) > 2:
            os.write(1, ("The System cannot find the path specidied ").encode())
            pass
        else:
            pid = os.getpid()
            rc = os.fork()

            if rc < 0:
                os.write(2, ("fork failed, returning %d\n" % rc).encode())
                sys.exit(1)
            elif rc == 0:
                args = [userInputList[0] ,userInputList[2]]
                os.close(1)
                os.open(userInputList[2], os.O_CREAT | os.WRONLY);
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

    elif '<' in userInputList:
        if len(userInputList) > 3:
            os.write(1, ("The System cannot find the path specidied ").encode())
            pass
        else:
            pid = os.getpid()
            rc = os.fork()

            if rc < 0:
                os.write(2, ("fork failed, returning %d\n" % rc).encode())
                sys.exit(1)
            elif rc == 0:
                args = [userInputList[2] ,userInputList[0]]
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


    elif '|' in userInputList:
        if len(userInputList) > 3:
            os.write(1, ("The System cannot find the path specidied ").encode())
            pass
        else:
            pid  = os.getpid()
            pr, pw = os.pipe()

            for f in (pr,pw):
                os.set_inheritable(f,True)

            rc = os.fork()

            if rc < 0:
                print("fork failed, returning %d\n" % rc, file=sys.stderr)
                pass

            elif rc == 0:
                args = [i.strip() for i in re.split('[\x7c]', userInput)]
                os.close(1)
                os.dup(pr,pw)
                os.set_inheritable(1, True)

                for fd in (pr,pw):
                    os.close(fd)
                newProcess(args[0].split())
            else:
                os.close(0)
                os.dup(pr)
                for fd in (pw, pr):
                    os.close(fd)
                newProcess(args[1].split())

    else:
        newProcess(userInputList)
