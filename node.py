from socketserver import ThreadingMixIn
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import psutil
import requests
import threading
import json
import uuid
import time
import random
import sys

DEFAULTNODEPORT = 14440;
DEFAULTWORKERPORT = 12220;
URL = "http://localhost";
ID = 0;
MAXID = 3
MAXWORKER = 5
WAIT = 5

REQUESTVOTE = 0
APPENDENTRY = 1
CPUSTATUS = 2
REQUESTVALUE = 3
ERRORCODE = 999


node = []
worker = []

leaderID = -999
hasVoted = 0
status = 0
starttime = None
timeout = 0
commitid = 999
commitload = 999

def randomTimeout():
    rand = random.uniform(1.5,4.7)
    print("Random called, timeout value" + str(rand))
    return rand

def init():
    if len(sys.argv)!=2:
        sys.exit("Please put 1 argument for ID")
    global ID
    ID = int(sys.argv[1])
    if ID > MAXID or ID < 0:
        sys.exit("Please put ID in range of 0 - MAXID")

    global node
    for i in range(MAXID):
        node.append(DEFAULTNODEPORT + i)
    for i in range(MAXWORKER):
        worker.append(999.9)

    global timeout
    timeout = randomTimeout()

    global starttime
    starttime = time.time()
    
def isTimeout():
    global starttime
    global timeout
    if time.time() > (starttime + timeout):
        return True
    else:
        return False

class NodeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            global node
            global worker

            global leaderID
            global hasVoted
            global status
            global timeout
            global commitid
            global commitload
            global starttime

            args = self.path.split('/')

            self.send_response(200)
            self.end_headers()

            if len(args) < 2:
                raise Exception()

            if args[1].isdigit():
                n = int(args[1])
                if n == REQUESTVOTE:
                    print("RequestVote")
                    if(hasVoted == 0):
                        hasVoted = 1
                        starttime = time.time()
                        self.wfile.write(str(ID).encode('utf-8'))
                    else:
                        self.wfile.write(str(ERRORCODE).encode('utf-8'))

                elif n==APPENDENTRY:
                    print("APPENDENTRY")
                    starttime = time.time()
                    status = 0
                    hasVoted = 0
                    leaderID = int(args[2])
                    starttime = time.time()
                    if len(args) == 5 :
                        worker[int(args[3])] = float(args[4])
                        print("LOAD for ID "+args[3]+"now is"+args[4])
                    self.wfile.write(str(ID).encode('utf-8'))

                elif n==CPUSTATUS:
                    print("CPUSTATUS")
                    commitid = int(args[2])
                    print("ID = " + str(commitid))
                    commitload = float(args[3])
                    print("LOAD = " + str(commitload))
                    print("WORKER COMMIT ID = " + str(worker[0]))
                    print("DONE")
                    if status==3:
                        worker[int(args[2])] = commitload
                    else:
                        requests.get(URL+":"+str(DEFAULTNODEPORT+leaderID)+"/"+str(CPUSTATUS)+"/"+args[2]+"/"+args[3])
                    self.wfile.write(str(ID).encode('utf-8'))

                elif n==REQUESTVALUE:
                    print("REQUESTVALUE")
                    leastCpuLoadId = 0
                    searchNumber = int(args[2])
                    for i in range(MAXWORKER):
                        if worker[i] < worker[leastCpuLoadId]:
                            leastCpuLoadId = i
                    requests.get(URL+":"+str(DEFAULTWORKERPORT+leastCpuLoadId)+"/"+str(searchNumber))
                    self.wfile.write(str(ID).encode('utf-8'))

                else :
                    raise Exception()

            else:
                raise Exception()

        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

class ThreadingServer(ThreadingMixIn,HTTPServer):
    pass

init()

print("You have ID:"+str(ID))
print("You are entering status:"+str(status))

# start the server in a background thread
server = ThreadingServer(('localhost',DEFAULTNODEPORT+ID),NodeHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()

time.sleep(WAIT)

while True:
    if isTimeout() and status == 0:
        print("Become Candidate")
        if leaderID != -999:
            timeout = randomTimeout()
        starttime = time.time()
        status = 1
        hasVoted = 1
        count = 1

    elif status == 1:
        print("Send Request Vote")
        status = 2
        for i in range(MAXID):
            if i != ID:
                print(URL+":"+str(DEFAULTNODEPORT+i)+"/"+str(REQUESTVOTE))

                try:
                    resp = requests.get(URL+":"+str(DEFAULTNODEPORT+i)+"/"+str(REQUESTVOTE))
                    if int(resp.text) < MAXID:
                        count += 1
                        print("YOU GOT A COUNT, NOW YOUR COUNT IS = " + str(count))
                except requests.exceptions.RequestException as e:
                    print ()
    elif status == 2:
        print("Checking Vote " + str(count) + "NEED " + str((MAXID//2)+1))
        if count >= (MAXID//2)+1:
            status = 3
        elif isTimeout():
            count = 0
            timeout = randomTimeout()
            starttime = time.time()
            hasVoted = 0
            status = 0
    elif status == 3:
        # print("Become Leader")
        count = 1
        for i in range(MAXID):
            if i!= ID:
                try:
                    print(str(commitid))
                    if commitid==999:
                        resp = requests.get(URL+":"+str(DEFAULTNODEPORT+i)+"/"+str(APPENDENTRY)+"/"+str(ID))
                    else:
                        print("Sending Load")
                        resp = requests.get(URL+":"+str(DEFAULTNODEPORT+i)+"/"+str(APPENDENTRY)+"/"+str(ID)+"/"+str(commitid)+"/"+str(commitload))
                    if int(resp.text) < MAXID:
                        count += 1
                except requests.exceptions.RequestException as e:
                    print ()
        if count < (MAXID//2)+1:
            status = 0
