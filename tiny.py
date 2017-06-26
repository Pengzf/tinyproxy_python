#coding=utf8
import socket, select
import sys
import thread
import ConfigParser
from multiprocessing import Process

class Proxy:
    def __init__(self, soc):
        self.client, _ = soc.accept()
        self.target = None
        self.BUFSIZE = 1024 * 4
        self.method = None
        self.http_port = None
        self.http_ip = None
        self.https_port = None
        self.https_ip = None
        self.http_first = None
        self.https_first=None
        config = ConfigParser.ConfigParser()
        config.read('tiny.conf')
        self.http_ip = str(config.get('http','ip'))
        self.http_port = int(config.get('http','port'))
        self.https_ip = str(config.get('https','ip'))
        self.https_port = int(config.get('https','port'))
        self.http_first = str(config.get('http','first'))
        self.https_first = str(config.get('https','first'))

    def header(self,request):
        if not request:
            return
        list = request.split('\n')
        firstLine = list[0]
        secondLine = list[1]
        host = secondLine.split(':')[1]
        line = firstLine.split()
        method = line[0]
        if method in ['GET', 'POST', 'PUT', "DELETE", 'HAVE']:
            url = line[1]
            version = line[2]
            tmp = url.split('/')
            ur = tmp[0] + '//' + tmp[2]
            uri = url.replace(ur, '')
            tmp = self.http_first
            tmp = tmp.replace('[Method]', method)
            tmp = tmp.replace('[Uri]', uri)
            tmp = tmp.replace('[Url]', url)
            tmp = tmp.replace('[Ur]', ur)
            tmp = tmp.replace('[Version]', version)
            tmp = tmp.replace('[Host]', host)
            tmp = tmp.replace('[N]', '\n')
            tmp = tmp.replace('[R]', '\r')
            tmp = tmp.replace('[T]', '\t')
            tmp = tmp.replace('[RN]', '\r\n')
            request=str(request).replace(firstLine+'\n'+secondLine,tmp)
        elif method == 'CONNECT':
            url = line[1]
            version = line[2]
            tmp = self.https_first
            tmp = tmp.replace('[Method]', method)
            tmp = tmp.replace('[Url]', url)
            tmp = tmp.replace('[Version]', version)
            tmp = tmp.replace('[Host]', host)
            tmp = tmp.replace('[N]', '\n')
            tmp = tmp.replace('[R]', '\r')
            tmp = tmp.replace('[T]', '\t')
            tmp = tmp.replace('[RN]', '\r\n')
            request = str(request).replace(firstLine + '\n' + secondLine, tmp)
        self.method = method
        return request

    def Method(self, request):
        self.target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.method in ['GET', 'POST', 'PUT', "DELETE", 'HAVE']:
            self.target.connect((self.http_ip, self.http_port))
        elif self.method == 'CONNECT':
            self.target.connect((self.https_ip, self.https_port))
        self.target.send(request)
        self.packet()

    def packet(self, timeout=1):
        inputs = [self.client, self.target]
        while True:
            readable, _, errs = select.select(inputs, [], inputs, timeout)
            if errs:
                break
            for packet in readable:
                try:
                    data = packet.recv(self.BUFSIZE)
                    if packet is self.client:
                        if self.method in ['GET', 'POST', 'PUT', "DELETE", 'HAVE']:
                            data=self.header(data)
                            self.target.send(data)
                        elif self.method == 'CONNECT':
                            self.target.send(data)
                    elif packet is self.target:
                        self.client.send(data)
                except:
                    break
        self.client.close()
        self.target.close()

    def run(self):
        request = self.client.recv(self.BUFSIZE)
        request = self.header(request)
        if request:
            self.Method(request)

if __name__ == '__main__':
    from multiprocessing import Process
    host = '127.0.0.1'
    port = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    try:
        while True:
            thread.start_new_thread(Proxy(server).run, ())
    except KeyboardInterrupt:
        server.close()
        sys.exit(0)
