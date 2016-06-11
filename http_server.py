#!/usr/bin/env python

import argparse
import psutil
import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 80

storedPIDs = []

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/cpu_info':
            self.send_response(200)
            self.send_header('Content-type', 'text')
            self.end_headers()
            self.wfile.write(str(psutil.cpu_percent()))
        elif self.path[0:10] == '/cpu_rate=':
            rate = int(self.path[10:])
            for pid in storedPIDs:
                subprocess.Popen(['kill', str(pid)])
            storedPIDs.append(subprocess.Popen(['python', 'controlCPURate.py', str(rate-2), str(rate+2), '10', '3', '0.001']).pid)
            self.send_response(200)
            self.send_header('Content-type', 'text')
            self.end_headers()
            self.wfile.write('Setting CPU load...')
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text')
            self.end_headers()
            self.wfile.write('Hello from server!')

class CustomHTTPServer(HTTPServer):
    def __init__(self, host, port):
        server_address = (host, port)
        HTTPServer.__init__(self, server_address, HTTPRequestHandler)

def run_server(port):
    try:
        server = CustomHTTPServer(DEFAULT_HOST, port)
        print "Custom HTTP server started on port: %s" % port
        server.serve_forever()
    except Exception, err:
        print "Error:%s" % err
    except KeyboardInterrupt:
        print "Server interrupted and is shutting down..."
        server.socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Customized HTTP Server')
    parser.add_argument('--port', action='store', dest='port', type=int, default=DEFAULT_PORT)
    given_args = parser.parse_args()
    port = given_args.port
    run_server(port)
