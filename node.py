from socketserver import ThreadingMixIn
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import psutil
import requests
import threading
import json
import uuid
import time

PORT = 12221;
URL = "";
ID = -999;
WAIT = 5;

def sendStatus():
    load = getCpuLoad();
    headers = {'content-type' : 'application/json'}
    data = {"load":load,"id":ID}
    requests.post(URL,data=data)

def getCpuLoad():
    return psutil.cpu_percent(interval=1)

class NodeHandler(BaseHTTPRequestHandler):
	def do_POST(self):
        try:
            content_len = int(self.headers.getheader('content-length', 0))
			post_body = self.rfile.read(content_len)

			print(post_body)
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

class ThreadingServer(ThreadingMixIn,HTTPServer):
    pass

if(ID==-999):
    ID = uuid.uuid4()

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
