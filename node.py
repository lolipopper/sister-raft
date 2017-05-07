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

timer = None
REQUESTVOTE = 0
APPENDENTRY = 1
CPUSTATUS = 2
REQUESTVALUE = 3
ERRORCODE = 999


node = []
worker = []

leaderID = 0
hasVoted = 0
status = 0
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
        node.append(DEFAULTWORKERPORT + i)

    global timeout
    timeout = randomTimeout()
    

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
                        timeout = randomTimeout()
                        self.wfile.write(str(ID).encode('utf-8'))
                    else:
                        self.wfile.write(str(ERRORCODE).encode('utf-8'))

                elif n==APPENDENTRY:
                    print("APPENDENTRY")
                    status = 0
                    hasVoted = 0
                    leaderID = args[2]
                    timeout = randomTimeout()
                    if len(args) == 5 :
                        commitid = args[3]
                        commitload = args[4]
                        worker[commitid] = commitload
                    self.wfile.write(str(ID).encode('utf-8'))

                elif n==CPULOAD:
                    print("CPULOAD")
                    commitid = args[2]
                    commitload = args[3]
                    if status==3:
                        worker[commitid] = commitload
                    else:
                        requests.get(URL+":"+str(DEFAULTNODEPORT+leaderID)+"/"+str(CPULOAD)+"/"+str(commitid)+"/"+str(commitload))
                    self.wfile.write(str(ID).encode('utf-8'))

                elif n==REQUESTVALUE:
                    print("REQUESTVALUE")
                    leastCpuLoadId = 0
                    searchNumber = args[2]
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
    print(str(timeout))
    if timeout < 0 and status == 0:
        print("Become Candidate")
        timeout = randomTimeout()
        status = 1
        hasVoted = 1
        count = 1

    elif status == 1:
        print("Send Request Vote")
        status = 2
        for i in range(MAXID):
            if i != ID:
                print(URL+":"+str(DEFAULTNODEPORT+i)+"/"+str(REQUESTVOTE))
                resp = requests.get(URL+":"+str(DEFAULTNODEPORT+i)+"/"+str(REQUESTVOTE))
                if int(resp.text) < MAXID:
                    count += 1
                    print("YOU GOT A COUNT, NOW YOUR COUNT IS = " + str(count))
    elif status == 2:
        print("Checking Vote " + str(count) + "NEED " + str((MAXID//2)+1))
        if count >= (MAXID//2)+1:
            status = 3
        elif timeout < 0:
            status = 0
    elif status == 3:
        print("Become Leader")
        count = 1
        for i in range(MAXID):
            if i!= ID:
                if commitid==999:
                    resp = requests.get(URL+":"+str(DEFAULTNODEPORT+i)+"/"+str(APPENDENTRY)+"/"+str(ID))
                else:
                    resp = requests.get(URL+":"+str(DEFAULTNODEPORT+i)+"/"+str(APPENDENTRY)+"/"+str(ID)+"/"+str(commitid)+"/"+str(commitload))
                if int(resp.text) < MAXID:
                    count += 1
        commitid = 999;
        if count < (MAXID//2)+1:
            status = 0


    timeout = timeout - 5

