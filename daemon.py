from socketserver import ThreadingMixIn
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import psutil
import requests
import threading
import json
import time
import random

PORT = 12220;
DEFAULTNODEPORT = 14440;
WORKERPORT = 13337;
CPUSTATUS = 2
URL = "http://localhost";
ID = 0;
MAXNODE = 3
WAIT = 5;

def sendStatus():
    load = getCpuLoad();
    for i in range(MAXNODE):
        try:
            r = requests.get(URL+":"+str(DEFAULTNODEPORT+i)+"/"+str(CPUSTATUS)+"/"+str(ID)+"/"+str(load))
            print(str(r.text))
        except requests.exceptions.RequestException as e:
            print()

def getCpuLoad():
    return psutil.cpu_percent(interval=1)

class DaemonHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            args = self.path.split('/')

            self.send_response(200)
            self.end_headers()

            if len(args) != 2:
                raise Exception()

            if args[1].isdigit():
                n = int(args[1])
                r = requests.get(URL+":"+str(WORKERPORT)+"/"+str(n))
                self.wfile.write((str(r.text)).encode('utf-8'))
            else:
                self.wfile.write(str(getCpuLoad()).encode('utf-8'))
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

class ThreadingServer(ThreadingMixIn,HTTPServer):
    pass

# start the server in a background thread
server = ThreadingServer(('localhost',PORT),DaemonHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()

while True:
    print (ID)
    sendStatus()
    print(str(getCpuLoad()))
    time.sleep(WAIT)
