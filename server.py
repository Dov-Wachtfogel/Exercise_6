#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


def average(lst):
    return sum(lst)/len(lst)


def get_analyze(get_message_path: str):
    if '?' in get_message_path:
        l = get_message_path.split('?')
        path = l[0]
        parms = l[1]
        parms_dict = eval('{"' + parms.replace('&', '","').replace('=', '":"') + '"}')
        return path, parms_dict
    else:
        return get_message_path, {}



class S(BaseHTTPRequestHandler):
    def _set_response(self, respone =200):
        self.send_response(respone)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        try:
            path, parms = get_analyze(str(self.path))
            parms = [float(i) for i in list(parms.values())]

        except:
            self._set_response(400)
            self.wfile.write(f'''
<html>
    <body>
        <h1> 400 error </h1 >
    <body>
</html>'''.encode('utf-8'))
        else:
            try:
                ans = eval(f'{path[1:]}({parms})')
            except:
                self._set_response(404)
                self.wfile.write(f'''
                <html>
                    <body>
                        <h1> 404 error </h1 >
                    <body>
                </html>'''.encode('utf-8'))
            else:
                self._set_response()
            self.wfile.write(f'''
<html>
    <body>
        <h1> The {path[1:]} of {str(parms)[1:-1]} is {ans} </h1 >
    <body>
</html>'''.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
