from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
import psutil
import requests

PORT = 12221;

class DaemonHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            r = requests.get("http://localhost:13337/2")
            self.send_response(200)
            self.end_headers()
            self.wfile.write((str(r.text)+ "&endl").encode('utf-8'))
            self.wfile.write(str(self.getCpuLoad()).encode('utf-8'))
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)
    def getCpuLoad(self):
        return psutil.cpu_percent(interval=1)


server = HTTPServer(("", PORT), DaemonHandler)
server.serve_forever()


