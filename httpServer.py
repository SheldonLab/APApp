import cgi
import json
import sys
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import traceback
from databaseUpload import DatabaseUpload
from chron_email_sender import RunEmail
data_path = '/data'
push_path = '/push'
host = "localhost"
user = "root"
password = "moxie100"
database = (host, user, password)


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        parsed_url = urlparse.urlparse(self.path)
        path = parsed_url.path
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        if path == data_path:
            if ctype == 'application/json':
                try:
                    data_string = self.rfile.read(int(self.headers['Content-Length']))
                    self.send_response(200)
                    self.end_headers()
                    data = json.loads(data_string)
                    uploader = DatabaseUpload(database, data)
                    uploader.start()
                    return
                except:
                    print traceback.print_exc()
                    self.send_error(500)
                    return
            # Bad request
            self.send_error(400)

        elif path == push_path:
            self.send_response(200)
            email = RunEmail(database)
            email.start()

        else:
            self.send_error(404)



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def httpServer(server_ip, port):
    server_address = (server_ip, port)
    httpd = ThreadedHTTPServer(server_address, RequestHandler)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    print 'use <Ctrl-C> to stop'
    httpd.serve_forever()
