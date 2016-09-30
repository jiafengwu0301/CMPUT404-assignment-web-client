#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# Modified by Jiafeng Wu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

# use urlparse to get host, path and port
# https://docs.python.org/2/library/urlparse.html
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def connect(self, host, port):
        # use sockets!

        # set the port as 80 if port is None
        if port == None:
            port = 80

        # https://docs.python.org/2/howto/sockets.html
        # create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to web server
        s.connect((host,port))
        return s

    # get the status code
    def get_code(self, data):
        lst = data.split()
        code = int(lst[1])
        return code

    # get the header
    def get_headers(self, data):
        lst = data.split("/r/n/r/n")
        headers = lst[0]
        return headers

    # get the body of html
    def get_body(self, data):
        lst = data.split("\r\n\r\n")
        body = lst[1]
        return body

    def httprequest(self,url, method,args=None):
        # if url not start with http://, then add it
        if not url.lower().startswith("http://"):
            url = "http://"+url

        # phase the url into several parts
        url_parse = urlparse(url)

        # get host, path, and port of url
        host = url_parse.hostname
        path = url_parse.path
        port = url_parse.port

        request = ""

        # set the http request for GET method
        if method.upper() == "GET":
            request = "GET " + path + " HTTP/1.1\r\n"
            request += "User-Agent: Web Client\r\n"
            request += "Host: " + host + "\r\n"
            request += "Accept: */*\r\n"
            request += "Connection: Close\r\n\r\n"

        # set the http request for POST method
        if method.upper() == "POST":
            args_encode = ""
            if args != None:
                args_encode = urllib.urlencode(args)

            request = "POST " + path +" HTTP/1.1\r\n"
            request += "Host: " + host + "\r\n"
            request += "Content-Type: application/x-www-form-urlencoded\r\n"
            request += "Content-Length: " +str(len(args_encode)) + "\r\n"
            request += "Accept: */*\r\n\r\n"
            request += args_encode +"\r\n"

        return host, port, request

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        method = "GET"

        # get host, post and request header
        host, port, request = self.httprequest(url, method,args)

        # connect to web server
        con = self.connect(host,port)

        # send the request header
        con.sendall(request)

        # receive the response from server
        response = self.recvall(con)

        # get the stats code, header and body of html
        code = self.get_code(response)
        header = self. get_headers(response)
        body = self.get_body(response)

        print response

        con.close

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        method = "POST"

        # get host, post and request header
        host, port, request = self.httprequest(url, method,args)

        # connect to web server
        con = self.connect(host,port)

        # send the request header
        con.sendall(request)

        # receive the response from server
        response = self.recvall(con)

        # get the stats code, header and body of html
        code = self.get_code(response)
        header = self. get_headers(response)
        body = self.get_body(response)

        con.close()

        print response

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )
