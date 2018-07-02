#!/bin/python3
import os
import sys
import pdb
from string import whitespace
import re


def getUser(machine):
    me = os.popen("whoami").readlines()[0][:-1]
    s = os.popen("ssh " + machine + " top -b -n 1").readlines()
    s = s[7:]
    users = []
    for line in s:
        line = line.split()
        user = line[1]
        if user not in users and re.match(r's[0-9]+', user) and not user == me:
        # if user not in users and re.match(r's[0-9]+', user):
            users.append(user)
    return users

def getUser1():
    me = os.popen("whoami").readlines()[0][:-1]
    s = os.popen("top -b -n 1").readlines()
    s = s[7:]
    users = []
    for line in s:
        line = line.split()
        user = line[1]
        if user not in users and re.match(r's[0-9]+', user) and not user == me:
        # if user not in users and re.match(r's[0-9]+', user):
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


def main(machine):
    users = getUser(machine)
    if len(users) == 0:
        print ("_")
    else:
        for user in users:
            print (getName(user))

def main1():
    users = getUser1()
    if len(users) == 0:
        print ("_")
    else:
        for user in users:
            print (getName(user))

if len(sys.argv) == 2:
    main(sys.argv[1])
elif len(sys.argv) == 1:
    main1()
else:
    print ("Too many args.")
