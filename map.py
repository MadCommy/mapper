#!/bin/python3
import subprocess
import bisect
import sys
import os
import time
import signal
import timeit
import pdb

username = "s1630747"

path = "/afs/inf.ed.ac.uk/user/s16/s1630747/myapps/map/"
roomPath = path + "rooms/"
imagePath = path + "images/"

whoat = "~/.local/bin/whoat"
mymachine = "cornet"
friendList = []
rooms = []
data = []
id = []
machineLen = 0
roomLen = 0
period = 600
wait = 60
timeout = 1

class Machine:
    def __init__(self, name, room):
        self.name = name
        self.room = room
        self.user = "."

    def __repr__(self):
        return self.name

    def updateUser(user):
        self.user = user

def init():
    initRooms()
    importFriends()
    del id[:]
    del data[:]
    for room in rooms:
        f = open(roomPath + room, "r")
        machines = str.split(f.read())

        for machine in machines:
            data.append(Machine(machine, room))
            id.append(machine)

        f.close()
    setLongest()

def update(room):
    backup()
    init()
    importData()
    f = open(roomPath + str(room), "r")
    machines = str.split(f.read())
    f.close()

    updateBack(machines)

def updateAll():
    init()
    machines = []
    for room in rooms:
        f = open(roomPath + str(room), "r")
        machines += str.split(f.read())
        f.close()

    return updateBack(machines)

def loop():
    while True:
        a = timeit.default_timer()
        v = updateAll()
        b = timeit.default_timer()
        if v == 0:
            continue
        t = b - a
        print ('Time: ' + str(t))
        if t >= period:
            t = period - wait
        time.sleep(period - t)

def updateBack(machines):
    i = 0
    for machine in machines:
        i += 1
        s = " " + machine + ": "

        # a = timeit.default_timer()
        try:
            user = subprocess.check_output(["ssh", machine, whoat], universal_newlines=True,timeout=timeout).rstrip()
            data[id.index(machine)].user = user
            s += "success"
        except Exception as ex:
            data[id.index(machine)].user = "?"
            s += "fail"
            print (ex)

        # b = timeit.default_timer()
        # time = b - a
        # s += " " + str(time)

        sys.stdout.write(str(i) + "/" + str(len(machines)) + s + " "*20 + "\r")
        sys.stdout.flush()
        signal.alarm(0)

    exportData()
    # os.system("ssh " + mymachine + " DISPLAY=:0 notify-send Map Updated &")
    print
    return 1

def initRooms():
    s = os.popen("ls " + roomPath).readlines()
    for i in range(len(s)):
        s[i] = s[i][:-1]
    global rooms
    rooms = s

def importData():
    init()
    f = open(path + "data", "r")
    first = True
    for line in f:
        if first:
            first = False
            continue
        s = str.split(line)
        machine = s[1]
        user = " ".join(s[2:])
        data[id.index(machine)].user = user
    f.close()

def exportData():
    f = open(path + "data", "w")
    f.write(time.ctime() + "\n")
    for machine in data:
        n = roomLen - len(str(machine.room))
        pad1 = " "*n
        n = machineLen - len(str(machine)) + 1
        pad2 = " "*n
        s = pad1 + str(machine.room) + ": " +  str(machine) + pad2 + str(machine.user) + "\n"
        f.write(s)
    f.close()

def importFriends():
    ls = os.popen("ls " + path).readlines()
    if "friends\n" not in ls:
        os.system("touch " + path + "friends")
        return
    f = open(path + "friends", "r")
    global friendList
    friendList = str.split(f.read())
    f.close()

def exportFriends():
    f = open(path + "friends", "w")
    for friend in friendList:
        f.write(friend + "\n")
    f.close()

def setLongest():
    mmax = 0
    rmax = 0
    for machine in data:
        l = len(machine.name)
        if l > mmax:
            mmax = l
    for room in rooms:
        l = len(room)
        if l > rmax:
            rmax = l

    global machineLen
    machineLen = mmax
    global roomLen
    roomLen = rmax

def getKey():
    proc = Popen(["kinit"], stdin=PIPE, stderr=PIPE)
    proc.stdin.write(password)
    os.system("aklog")

def reset():
    init()
    exportData()

def backup():
    os.system("cp " + path + "data " + path + "data.bak")
    os.system("cp " + path + "friends " + path + "friends.bak")

def restore():
    os.system("cp " + path + "data.bak " + path + "data")
    os.system("cp " + path + "friends.bak " + path + "friends")

def search(q):
    q = "\"" +  ".*".join(q) + "\""
    s = "grep -i " + q + " " + path + "data | less"
    os.system(s)

def show(room):
    os.system("feh " + imagePath + room + ".png &")

def friends():
    if len(friendList) < 2:
        for friend in friendList:
            search(friend)
        return
    q = "\|".join(friendList)
    q = "\"" + q + "\""
    os.system("grep -i " + q + " " + path + "data | less")

def add(friend):
    if friend not in friendList:
        bisect.insort(friendList, friend)
        print (getName(friend) + ": added.")
    else:
        print (getName(friend) + ": already in system.")
    exportFriends()

def remove(friend):
    if friend in friendList:
        friendList.remove(friend)
        print (getName(friend) + ": removed.")
    else:
        print (getName(friend) + ": not in system.")
    exportFriends()

def getName(id):
    s = os.popen("finger " + id).readlines()[0]
    s = " ".join(str.split(s)[3:])
    return s

def listFriends():
    importFriends()
    out = []
    first = True
    s = ""
    for friend in friendList:
        if first:
            s = "echo " + friend + " " + getName(friend) + " > " + path + "friendsHR"
            first = False
        else:
            s = "echo " + friend + " " + getName(friend) + " >> " + path + "friendsHR"
        os.system(s)
    os.system("less " + path + "friendsHR")

def view():
    os.system("less " + path + "data")

def getTime():
    os.system("head -1 " + path + "data")

def main():
    init()
    numArgs = len(sys.argv) - 1
    if numArgs > 0:
        if str(sys.argv[1]) == "update" and numArgs == 2:
            update(str(sys.argv[2]))
        elif str(sys.argv[1]) == "update" and numArgs == 1:
            updateAll()
        elif str(sys.argv[1]) == "restore":
            restore()
        elif str(sys.argv[1]) == "reset":
            reset()
        elif str(sys.argv[1]) == "backup":
            backup()
        elif str(sys.argv[1]) == "v":
            view()
        elif str(sys.argv[1]) == "s" and numArgs >= 2:
            q = sys.argv[2:]
            search(q)
        elif str(sys.argv[1]) == "loop":
            loop()
        elif str(sys.argv[1]) == "d" and numArgs == 2:
            show(str(sys.argv[2]))
        elif str(sys.argv[1]) == "f":
            friends()
        elif str(sys.argv[1]) == "lf":
            listFriends()
        elif str(sys.argv[1]) == "a" and numArgs == 2:
            add(str(sys.argv[2]))
        elif str(sys.argv[1]) == "r" and numArgs == 2:
            remove(str(sys.argv[2]))
        elif str(sys.argv[1]) == "t":
            getTime()
    else:
        loop()

main()
