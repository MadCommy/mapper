#!/bin/python3
import os
import sys
import pdb
from string import whitespace
import re


def getUser(remote, machine):
    me = os.popen("whoami").readlines()[0][:-1]
    if remote:
        s = os.popen("ssh " + machine + " loginctl").readlines()
    else:
        s = os.popen("loginctl").readlines()

    s = s[1:-2]
    users = []
    for line in s:
        line = line.split()
        user = line[2]
        if user not in users and "seat0" in line:
            users.append(user)
    return users

def getName(uun):
    s = os.popen("finger " + uun).readlines()
    s = s[0].split()
    out = ""
    out += uun
    for word in s[3:]:
        out += " " + word
    return out


def main(remote, machine):
    users = getUser(remote, machine)
    if len(users) == 0:
        print ("_")
    else:
        for user in users:
            if (users.index(user) == 0):
                print (getName(user)),
            else:
                print "; " + (getName(user)),
        print

if len(sys.argv) == 2:
    main(True, sys.argv[1])
elif len(sys.argv) == 1:
    main(False, "")
else:
    print ("Too many args.")
