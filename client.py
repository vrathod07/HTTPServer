import gzip
from socket import *
import sys
from pathlib import Path
from threading import *
import  subprocess

#consatnts
server = "localhost"
PORT = 8000



def serve(server,PORT):

    try:
        clientSocket = socket(AF_INET,SOCK_STREAM)
        clientSocket.connect((server,PORT))

        validate_get(clientSocket)
        validate_HEAD(clientSocket)
        validate_post(clientSocket)
        validate_put(clientSocket)
        validate_delete(clientSocket)
        validate_501(clientSocket)
    except:
        print("disconnected")
        sys.exit(0)

def file_return(file_type):
    # assign directory
    directory = '/htdocs'
    # iterate over files in that directory
    files = Path(directory).glob(file_type)
    for file in files:
        return file

def validate_get(clientSocket):

    m = 'GET /write.txt HTTP/1.1\r\n'
    m += 'Host: 127.0.0.1:8000\r\n'
    m += 'User-Agent: CLIENT\r\n'
    m += 'Content-Type: text/html\r\n'
    m += 'Connection: Keep Alive\r\n'
    m += 'Content-Length: 55\r\n'
    m += '\r\n'

    m1 = 'GET /index.html HTTP/1.1\r\n'
    m1 += 'Host: 127.0.0.1:8000\r\n'
    m1 += 'User-Agent: CLIENT\r\n'
    m1 += 'Content-Type: text/html\r\n'
    m1 +=  'Connection: Keep Alive\r\n'
    m1 += 'Content-Length: 55\r\n'
    m1 += '\r\n'

    m2 = 'GET /song.mp3 HTTP/1.1\r\n'
    m2 += 'Host: 127.0.0.1:8000\r\n'
    m2 += 'User-Agent: CLIENT\r\n'
    m2 += 'Content-Type: text/html\r\n'
    m2 += 'Connection: Keep Alive\r\n'
    m2 += 'Content-Length: 55\r\n'
    m2 += '\r\n'

    m3 = 'GET /empty.html HTTP/1.1\r\n'
    m3 += 'Host: 127.0.0.1:8000\r\n'
    m3 += 'User-Agent: CLIENT\r\n'
    m3 += 'Content-Type: text/html\r\n'
    m3 += 'Connection: Keep Alive\r\n'
    m3 += 'Content-Length: 55\r\n'
    m3 += '\r\n'

    try:
        clientSocket.send(m.encode())
        print_data(clientSocket)
        print('Successfully validated GET')
    except Exception as e:
        print(e)

def validate_HEAD(clientSocket):
    m = 'HEAD /hello.html HTTP/1.1\r\n'
    m += 'Host: 127.0.0.1:8888\r\n'
    m += 'User-Agent: Auto Tester\r\n'
    m += 'Content-Type: application/x-www-form-urlencoded\r\n'
    m += 'Connection: Close\r\n'
    m += 'Content-Length: 55\r\n'
    m += '\r\n'

    m1 = 'HEAD /write.txt HTTP/1.1\r\n'
    m1 += 'Host: 127.0.0.1:8888\r\n'
    m1 += 'User-Agent: Auto Tester\r\n'
    m1 += 'Content-Type: application/x-www-form-urlencoded\r\n'
    m1 +=  'Connection: Keep Alive\r\n'
    m1 += 'Content-Length: 55\r\n'
    m1 += '\r\n'

    try:
        clientSocket.send(m.encode())
        print_data(clientSocket)
        print('Successfully validated HEAD')
    except Exception as e:
        print(e)



def validate_post(clientSocket):
    m_a = 'name=Vaishnavi+Rathod&email=rathodvs19.comp%40coep.ac.in'
    msg_text = 'name=Vaishnavi Rathod&email=rathodvs19.comp@coep.ac.in'
    m_b = '--boundary\nContent-Disposition: form-data; name="name"\n\nVaishnavi Rathod\n'
    m_b += '--boundary\nContent-Disposition: form-data; name="email"\n\nrathodvs19.comp@coep.ac.in\n'
    m_b += '--boundary--'


    m = 'POST /hello.html'+ ' HTTP/1.1\r\n'
    m += 'Host: localhost\r\n'
    m += 'User-Agent: localhost\r\n'
    m += 'Content-Type: ' + 'text/plain\r\n'
    m += 'Content-Length: ' + str(len(msg_text)) + '\r\n'
    m += 'Connection: Keep Alive\r\n'
    m += '\r\n'
    m += msg_text

    m1 = 'POST /form2.html HTTP/1.1'
    m1 += 'Host: localhost'
    m1 += 'User-Agent: localhost\r\n'
    m1 += 'Content-Type: ' + 'multipart/form-data;boundary=boundary' +"\r\n"
    m1 += 'Connection: Close\r\n'
    m1 += 'Content-Length: ' + str(len(m_b)) + '\r\n'
    m1 += '\r\n'
    m1 += m_b

    m2 = 'POST /form3.html HTTP/1.1'
    m2 += 'Host: localhost'
    m2 += 'User-Agent: localhost\r\n'
    m2 += 'Content-Type: ' + 'application/x-www-form-urlencoded' +"\r\n"
    m2 += 'Content-Length: ' + str(len(m_b)) + '\r\n'
    m2 += '\r\n'
    m2 += m_a


    try:
        clientSocket.send(m1.encode())
        print_data(clientSocket)
        print('Successfully validated POST')

    except Exception as e:
        print(e)

def validate_put(clientSocket):
    m_a = 'name=Vaishnavi+Rathod&email=rathodvs19.comp%40coep.ac.in'
    msg_text = 'name=Vaishnavi Rathod&email=rathodvs19.comp@coep.ac.in'
    m_b = '--boundary\nContent-Disposition: form-data; name="name"\n\nVaishnavi Rathod\n'
    m_b += '--boundary\nContent-Disposition: form-data; name="email"\n\nrathodvs19.comp@coep.ac.in\n'
    m_b += '--boundary--'


    m = 'PUT /hello.html'+ ' HTTP/1.1\r\n'
    m += 'Host: localhost\r\n'
    m += 'User-Agent: localhost\r\n'
    m += 'Content-Type: ' + 'text/plain\r\n'
    m += 'Content-Length: ' + str(len(msg_text)) + '\r\n'
    m += '\r\n'
    m += msg_text

    m1 = 'PUT /form2.html HTTP/1.1'
    m1 += 'Host: localhost'
    m1 += 'User-Agent: localhost\r\n'
    m1 += 'Content-Type: ' + 'multipart/form-data;boundary=boundary' +"\r\n"
    m1 += 'Content-Length: ' + str(len(m_b)) + '\r\n'
    m1 += '\r\n'
    m1 += m_b

    m2 = 'PUT /form3.html HTTP/1.1'
    m2 += 'Host: localhost'
    m2 += 'User-Agent: localhost\r\n'
    m2 += 'Content-Type: ' + 'application/x-www-form-urlencoded' +"\r\n"
    m2 += 'Content-Length: ' + str(len(m_b)) + '\r\n'
    m2 += '\r\n'
    m2 += m_a


    try:
        clientSocket.send(m.encode())
        print_data(clientSocket)
        print('Successfully validated PUT')

    except Exception as e:
        print(e)

def validate_delete(clientSocket):

    m = 'DELETE /POST/HTML/hello.txt HTTP / 1.1\r\n'
    m += 'Host: localhost\r\n'
    m += 'Accept: text/html\r\n'
    m += 'Content-Type: text/html'
    try:
        clientSocket.send(m.encode())
        print_data(clientSocket)
        print('Successfully validated DELETE')
    except Exception as e:
        print(e)

def print_data(clientSocket):
    try:
        data = clientSocket.recv(770000)
        data_new = data.split(b'\r\n\r\n')

        if data_new[1] == b'':
            print(data_new[0].decode())
        else:
            print(gzip.decompress(data_new[1]).decode())

    except Exception as e:
        print(e)

def validate_cookies():
    try:
        f = open('Cookies/cookie.txt','r')
        content = f.read()
        print('This is the content in the cookie file: \n')
        print(content)
        f.close()
    except:
        print('File not found!')

def validate_log():
    try:
        f = open('log/access.txt','r')
        content = f.read()
        print('This is the content in the access log file: \n')
        print(content)
        f.close()
    except:
        print('File not found!')
    try:
        f = open('log/error.txt', 'r')
        content = f.read()
        print('This is the content in the error log file: \n')
        print(content)
        f.close()
    except:
        print('File not found!')

def validate_501(clientSocket):

    m = 'METHOD /POST/HTML/hello.txt HTTP / 1.1\r\n'
    m += 'Host: localhost\r\n'
    m += 'Accept: text/html\r\n'
    m += 'Content-Type: text/html'
    try:
        clientSocket.send(m.encode())
        print_data(clientSocket)
        print('Successfully validated 501')
    except Exception as e:
        print(e)

serve(server,PORT)