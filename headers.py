import os
import mimetypes
import datetime
import  time

class Headers:


    def get_headers(self, headers, extra=None):
        headers_new = ""
        for a in headers:
            if headers[a]:
                headers_new += a + ":" + headers[a] + "\r\n"
        if extra:
            for b in extra:
                if extra[b]:
                    print(b,extra[b])
                    headers_new += b + ":" + extra[b] + "\r\n"
        return headers_new

    def get_extra_headers(self,request):
        extra_headers = dict()
        new_headers = dict()

        readlines = request.split('\r\n')
        readlines = readlines[1:len(readlines)-2]

        for line in readlines:
            header = line.split(':',1)
            if len(header) > 2:
                extra_headers.update({header[0]: header[1]})
        new_headers = self.create_dict(request,extra_headers)
        return new_headers

    def create_dict(self,request,extra_headers):
            new_headers = dict()

            headers = request.split('\n')
            filename = headers[0].split(' ')[1]
            path = 'htdocs'+filename

            if filename == '/':
                filename = '/index.html'
            filetype = mimetypes.guess_type(filename)[0] or 'text/html'
            try:
                if filetype == 'text/html' or 'text/plain':
                    fin = open('htdocs/' + filename)
                    Content_Location = 'htdocs/' + filename
                else:
                    fin = open('assets/' + filename)
                    Content_Location = 'assets/' + filename

                content = fin.read()
                length = str(len(content))
                new_headers.update({'Content-type': filetype})
                new_headers.update({'Content-Length': length})
                fin.close()

            except:

                content = b'HTTP/1.0 404 NOT FOUND\n\n<h1>File Not Found</h1>'
                length = str(len(content))
                new_headers.update({'Content-Length': length})
                Content_Location = 'Null'

            if os.path.exists(path):
                last_mod = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(os.path.getmtime('htdocs' + filename)))
                expires = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(time.time() + 1000))
                new_headers.update({'Expires': expires})
                new_headers.update({'Last-Modified': last_mod})


            # Date retrieval
            x = datetime.datetime.now()

            YEAR = x.year
            DAY = x.strftime("%a")
            DATE = x.strftime("%d")
            MONTH = x.strftime("%b")
            TIME = x.strftime("%X")
            y = str(DAY)+", "+str(DATE)+" "+str(MONTH)+" "+str(YEAR)+" "+str(TIME)+" GMT"



            host = extra_headers.get('Host')
            user = extra_headers.get('User-Agent')
            acpt = extra_headers.get('Accept')
            acpt_enco = extra_headers.get('Accept-Encoding')
            conn = extra_headers.get('Connection')



            new_headers.update({'host':host})
            new_headers.update({'User-Agent':user})
            new_headers.update({'Accept':acpt})
            new_headers.update({'Accept-Enco':acpt_enco})
            new_headers.update({"Date":y})
            new_headers.update({'Connection':conn})
            new_headers.update({'Content_Location: ':Content_Location})
            new_headers.update({'Allow':'GET, POST, PUT, DELETE, HEAD'})

            return new_headers

