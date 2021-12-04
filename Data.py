from main import *
from datetime import datetime
import numpy as np

def save_cookies(addr):
    path = "Cookies/cookie.txt"
    try:
        f = open(path, "r+")
        while True:
            data = f.readline()
            if data.strip("\n") == str(addr):
                print("Cookie present")
                count = f.readline()
                f.seek(f.tell() - len(count))
                f.write(str(int(count) + 1))
                break
            elif data == '':
                f.write(str(addr) + '\n')
                f.write('1\n')
                break
        f.close()
    except:
        raise FileExistsError

def do_LOG(addr, request,response,level): #1: max logging  #2:  intermediate #3: basic logging

    path = 'log/logs.txt'
    now = datetime.now()
    methods = request.split("\r\n")[0]
    user_agent = request.split("\r\n")[3]
    status_code = response[9:12].decode()
    randno = np.random.randint(1000, 9000)
    print(randno)
    line_3 = str(addr) + " " + str(now) + " " + str(methods) + "\n"
    line_2 = str(addr) + " " + str(now) + " " + str(methods) + " " + str(status_code) + " " + str(randno) + "\n"
    line_1 = str(addr) + " " + str(now) + " " + str(methods) + " " + str(status_code) + " " + str(randno) + " " + str(user_agent) + "\n"
    try:
        f = open(path, "a")
        if level == 3:
            f.write(line_3)
            f.close()
        if level == 2:
            f.write(line_2)
            f.close()
        if level == 1:
            f.write(line_1)
            f.close()
    except:

        raise FileExistsError


def do_errorLog(data,addr):
    path = 'log/error_logs.txt'
    try:
        f = open(path,"a")
        now = datetime.now()
        data = str(now)+" "+str(addr)+" "+str(data)
        f.write(data)
        f.close()
    except:
        raise FileExistsError