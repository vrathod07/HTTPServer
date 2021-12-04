import mimetypes
from Data import *
from get_config import *
from socket import *
from headers import *
from status_code import *
import os
from threading import *
import sys
import time
import traceback
import gzip
import re

# CONSTANTS
server = HOST
PORT = 8000
STAT = sys.argv[1]
TIMEOUT = TIMEOUT
MAX_CONNECTIONS = CONNECTIONS
MAX_REQUEST = MAX_REQUEST
BUFFER = BUFFER

class TCPServer():

    def __init__(self, host='127.0.0.1', port=PORT):
        self.host = host
        self.port = port

    def identify_attributes(self,request):
        try:
            readlines = request.split('\r\n')
            line = readlines[0].split(' ')
            method = line[0]
            filename = line[1]
            HTTP_Version = line[2]
            indx = request.find('Connection: ')
            if indx != -1:
                conn = request[indx:].split('\n')[0].split(':')[1].replace(" ","")
            else:
                conn = 'Close'
        except:
            method = None
            filename = None
            HTTP_Version = '1.1'
            conn = 'Close'
        return method,filename,HTTP_Version,conn

    def serve(self, connectionSocket, addr):
        while True:
            request = connectionSocket.recv(BUFFER).decode()
            method, filename, Version, conn = self.identify_attributes(request)

            try:
                if method:
                    if method == 'GET':
                        response = self.hanle_GET(request)

                    elif method == 'POST':
                        response = self.handle_POST(request)

                    elif method == 'PUT':
                        response = self.handle_PUT(request)

                    elif method == 'HEAD':
                        response = self.handle_HEAD(request)

                    elif method == 'DELETE':
                        response = self.handle_DELETE(request)
                    else:
                        response = self.handle_501(request)
                else:
                    response = b'<h1>Some Error Occured</h1>'
                    do_errorLog('Some Error Occured',addr)

                connectionSocket.sendall(response)
                do_LOG(addr,request,response, 3)
                print(f'This is connection:{conn}')
                if conn.replace(" ", "") == "Close":
                    connectionSocket.close()
                    print('Socket CLosed')
                elif conn == "Keep ALive":
                    print('Connection is persistent')
                    connectionSocket.settimeout(TIMEOUT)
            except timeout:
                print('Socket timeout, loop and try recv() again')
                do_errorLog('Socket timeout, loop and try recv() again',addr)
                continue

    def startServer(self):

        serverSocket = socket(AF_INET, SOCK_STREAM)
       # serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSocket.bind((self.host, self.port))
        serverSocket.listen(MAX_CONNECTIONS)
        print('Listening on port %s ...' % PORT)

        while True:
            print("Server started!!")
            try:
                connectionSocket, addr = serverSocket.accept()

                th = Thread(target=self.serve, args=[connectionSocket, addr])
                th.start()
                save_cookies(addr)

            except error:
                print('Socket connect failed! Loop up and try socket again')
                traceback.print_exc()
                do_errorLog('Socket connect failed! Loop up and try socket again',addr)
                continue

    def hanle_request(self, data,request):
        return data

    def hanle_GET(self, request):
        return request

    def handle_POST(self, request):
        return request

    def handle_HEAD(self,data):
        return data

    def handle_PUT(self,data):
        pass

    def handle_DELETE(self,data):
        pass

    def handle_501(self, request):
        pass


class HTTPServer(TCPServer):
    header = {"Content-Encoding":"utf-8",
              "Host":"Localhost",
              "Allow": "GET, POST, HEAD, PUT, DELETE",
              "Accept-Charset":"utf-8",
              "charset":"utf-8",
              "Server":"VHHTPServer"}

    def hanle_request(self, data, request):

        head = Headers()
        extra_headers = head.get_extra_headers(request=request)
        headers = head.get_headers(headers=self.header,extra=extra_headers)

        response_line = get_response_line(200)

        blank_line = b"\r\n"

        response_body = gzip.compress(data)
        return b"".join([response_line, headers.encode(), blank_line, response_body])

    def hanle_GET(self, request):
        # Parse HTTP headers
        headers = request.split('\n')
        filename = headers[0].split(' ')[1]

        # Get the content of the file
        if filename == '/':
            filename = '/index.html'

        filetype = mimetypes.guess_type(filename)[0] or 'text/html'

        try:
            if filetype == 'text/html' or 'text/plain':
                fin = open('htdocs' + filename,'rb')
                content = fin.read()
                fin.close()
            else:
                fin = open('assests'+filename,'rb')
                content = fin.read()
                fin.close()
            if content == b'':
                head = Headers()
                headers = head.get_headers(headers=self.header)
                response_line = get_response_line(204)
                blank_line = b"\r\n"
                response_body = gzip.compress(b'<h1>NO CONTENT</h1>')
                response = b"".join([response_line, headers.encode(), blank_line, response_body])
            else:
                response = self.hanle_request(content,request)


            if filename[-1] == '/':
                response = b'HTTP / 1.1 301 Moved Permanently\n Location: htdocs/index.html'

        except FileNotFoundError:
            head = Headers()
            extra_headers = head.get_extra_headers(request=request)
            headers = head.get_headers(headers=extra_headers)
            response_line = get_response_line(404)
            blank_line = b"\r\n"
            response_body = gzip.compress(b'HTTP/1.0 404 NOT FOUND\n\n<h1>File Not Found</h1>')
            response = b"".join([response_line, headers.encode(), blank_line, response_body])

        return response


    def handle_HEAD(self,request):
        headers = request.split('\n')
        filename = headers[0].split(' ')[1]

        # Get the content of the file
        if filename == '/':
            filename = '/index.html'

        head = Headers()
        extra_headers = head.get_extra_headers(request=request)
        headers = head.get_headers(headers=extra_headers)
        response_line = get_response_line(200)
        blank_line = b"\r\n"

        response = b"".join([response_line, headers.encode(), blank_line])

        if filename[-1] == '/':
            response = 'HTTP / 1.1 301 Moved Permanently\n Location: htdocs/index.html'

        return  response


    def handle_POST(self, request):

        headers = request.split('\n')
        filename = headers[0].split(' ')[1]
        data = headers[-1].split('&')
       # print(f'This is data: {data}')

        head = {}
        lines = request.split('\r\n')
        lines = lines[1: len(lines) - 2]
        for line in lines:
            splited = line.split(': ', 1)
            head.update({splited[0]: splited[1]})
        enc = head.get('Content-Type')

        # Get the content of the file
        if filename == '/':
            filename = '/index.html'
        filename = filename.replace('.html','.txt')

        filetype = mimetypes.guess_type(filename)[0] or 'text/html'

        try:
            if enc == 'text/plain':
                f = open(('POST/HTML' + filename),'a')
                key = []
                value = []
                for i in data:
                    dict = i.split('=')
                    key.append(dict[0])
                    value.append(dict[1])
                   # print(f'This is the key: {key} and this is the value: {value}')
                f.write(f'This is the key: {key} and this is the value: {value}\n')
                f.close()

                content = b'HTTP/1.0 200 OK\n\n<h1>DATA POSTED</h1>'
                response = self.hanle_request(content, request)
            elif enc.split(';')[0] == 'multipart/form-data':
                f = open(('POST/HTML' + filename), 'a')
                boundary = enc.split(';')[1].split('=')[1]

                c_dispo = request.find('Content-Disposition')
                last_boundary = request.find('--'+boundary+'--')
                matches = re.finditer('Content-Disposition',request)
                matches_positions = [match.start() for match in matches]
                key = []
                value = []
                for i in matches_positions:
                    key.append(request[i:].split(boundary)[0].split('\n\n')[0].split(';')[1].split('=')[1])
                    value.append(request[i:].split(boundary)[0].split('\n\n')[1].split('\n')[0])

                f.write(f'This is the key: {key} and this is the value: {value}\n')
                f.close()
                content = b'HTTP/1.0 202 OK\n\n<h1>DATA POSTED</h1>'
                response = self.hanle_request(content, request)

            elif enc == 'application/x-www-form-urlencoded':
                f = open(('POST/HTML' + filename), 'a')
                key = []
                value = []
                for i in data:
                    dict = i.split('=')
                    key.append(dict[0])
                    f2 = dict[1].find('+')
                    if f2 != -1:
                     dict[1] =  dict[1].replace('+',' ')
                    f1 = dict[1].find('%')
                    if f1 != -1:
                       dict[1] =  dict[1].replace(dict[1][f1:f1 + 3], bytes.fromhex(dict[1][f1 + 1:f1 + 3]).decode('utf-8'))
                    value.append(dict[1])

                f.write(f'This is the key: {key} and this is the value: {value}\n')
                f.close()

                content = b'HTTP/1.0 202 OK\n\n<h1>DATA POSTED</h1>'
                response = self.hanle_request(content, request)
            elif enc.split('/')[0] == 'image':
                f = open((('assets/' + filename)), 'wb')
                f.write(data)
                f.close()
            else:
                content = b'HTTP/1.0 200 OK\n\n<h1>NO DATA POSTED</h1>'
                response = self.hanle_request(content,request)

        except FileNotFoundError:
            head = Headers()
            extra_headers = head.get_extra_headers(request=request)
            headers = head.get_headers(headers=extra_headers)
            response_line = get_response_line(404)
            blank_line = b"\r\n"
            response_body = gzip.compress(b'HTTP/1.0 404 NOT FOUND\n\n<h1>File Not Found</h1>')
            response = b"".join([response_line, headers.encode(), blank_line, response_body])

        return response



    def handle_PUT(self,request):

        headers = request.split('\n')
        filename = headers[0].split(' ')[1]
        data = headers[-1].split('&')
        # print(f'This is data: {data}')

        head = {}
        lines = request.split('\r\n')
        lines = lines[1: len(lines) - 2]
        for line in lines:
            splited = line.split(': ', 1)
            head.update({splited[0]: splited[1]})
        enc = head.get('Content-Type')
        # print("This is the encoding:",enc)

        # Get the content of the file
        if filename == '/':
            filename = '/index.html'
        filename = filename.replace('.html', '.txt')

        filetype = mimetypes.guess_type(filename)[0] or 'text/html'
       # print(f'This is the type: {filetype}')
        try:
            if enc == 'text/plain':
                f = open(('PUT' + filename), 'w')
                key = []
                value = []
                for i in data:
                    dict = i.split('=')
                    key.append(dict[0])
                    value.append(dict[1])
                # print(f'This is the key: {key} and this is the value: {value}')
                f.write(f'This is the key: {key} and this is the value: {value}\n')
                f.close()

                content = b'HTTP/1.0 200 OK\n\n<h1>DATA POSTED</h1>'
                response = self.hanle_request(content, request)
            elif enc.split(';')[0] == 'multipart/form-data':
                pass
            elif enc == 'application/x-www-form-urlencoded':
                pass
            elif enc.split('/')[0] == 'image':
                f = open((('PUT' + filename)), 'wb')
                f.write(data)
                f.close()
            else:
                content = b'HTTP/1.0 200 OK\n\n<h1>NO DATA POSTED</h1>'
                response = self.hanle_request(content, request)

        except FileNotFoundError:
            head = Headers()
            extra_headers = head.get_extra_headers(request=request)
            headers = head.get_headers(headers=extra_headers)
            response_line = get_response_line(404)
            blank_line = b"\r\n"
            response_body = gzip.compress(b'HTTP/1.0 404 NOT FOUND\n\n<h1>File Not Found</h1>')
            response = b"".join([response_line, headers.encode(), blank_line, response_body])

        return response

    def handle_DELETE(self,request):

        # Parse HTTP headers
        headers = request.split('\n')
        filename = headers[0].split(' ')[1]
        filetype = mimetypes.guess_type(filename)[0] or 'text/html'
        # Get the content of the file
        if filename == '/index.html':
            head = Headers()
            extra_headers = head.get_extra_headers(request=request)
            headers = head.get_headers(headers=extra_headers)
            response_line = get_response_line(404)
            blank_line = b"\r\n"
            response_body = gzip.compress(b'HTTP/1.0 404 NOT FOUND\n\n<h1>Permission Denied</h1>')
            response = b"".join([response_line, headers.encode(), blank_line, response_body])
        else:
            if filename.split('.')[1] == 'html':
                path = 'htdocs/'+filename
            else:
                path = filename[1:]

            if os.path.exists(path):
                os.remove(path)
                try:
                    fin = open('htdocs/delete.html', 'rb')
                    content = fin.read()
                   # print(f'This is the contet: {content}')
                    fin.close()
                    response = self.hanle_request(content, request)

                except FileNotFoundError:
                    f = open('htdocs/delete.html','wb')
                    f.write(b'<html>\n<body>\n<h1>File deleted.</h1>\n</body>\n</html>')
                    f.close()
                    head = Headers()
                    extra_headers = head.get_extra_headers(request=request)
                    headers = head.get_headers(headers=extra_headers)
                    response_line = get_response_line(404)
                    blank_line = b'\r\n'
                    response_body = gzip.compress(b'HTTP/1.0 404 NOT FOUND\n\n<h1>File Deleted</h1>')
                    response = b"".join([response_line, headers.encode(), blank_line, response_body])
            else:
                head = Headers()
                extra_headers = head.get_extra_headers(request=request)
                headers = head.get_headers(headers=extra_headers)
                response_line = get_response_line(404)
                blank_line = b"\r\n"
                response_body = gzip.compress(b'HTTP/1.0 404 NOT FOUND\n\n<h1>File Not Found</h1>')
                response = b"".join([response_line, headers.encode(), blank_line, response_body])



        return response

    def handle_501(self,request):
        head = Headers()
        extra_headers = head.get_extra_headers(request=request)
        headers = head.get_headers(headers=extra_headers)
        response_line = get_response_line(501)
        blank_line = b"\r\n"
        response_body = gzip.compress(b'HTTP/1.0 501 \n\n<h1>Method not Implemented</h1>')
        response = b"".join([response_line, headers.encode(), blank_line, response_body])

        return response
if __name__ == '__main__':
    if STAT == 'start':
        server = HTTPServer()
        server.startServer()
    if STAT == 'stop':
        print("Server shutdown")
        sys.exit(0)
    if STAT == 'stop':
        sys.exit(0)
