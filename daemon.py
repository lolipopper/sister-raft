from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import psutil
import requests

PORT = 12221;

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
                r = requests.get("http://localhost:13337/"+str(n))
                self.wfile.write((str(r.text)).encode('utf-8'))
            else:
                self.wfile.write(str(self.getCpuLoad()).encode('utf-8'))
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)
    def getCpuLoad(self):
        return psutil.cpu_percent(interval=1)

server = HTTPServer(("", PORT), DaemonHandler)
server.serve_forever()


