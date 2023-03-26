import select
import socket
import sys
from threading import Thread
from configparser import ConfigParser

# For directory listing
from os import listdir
from os.path import exists

config_object = ConfigParser()
config_object.read("httpserver.conf")
userinfo = config_object["Server"]
HOST = userinfo.get('host')
PORT = int(userinfo.get("port"))


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        input_list = [self.server]
        try:
            while True:
                input_ready, _, _ = select.select(input_list, [], [])

                for s in input_ready:

                    if s == self.server:
                        # handle the server socket
                        client_socket, client_address = self.server.accept()
                        c = Client(client_socket, client_address)
                        c.start()
                        self.threads.append(c)
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
        finally:
            self.server.close()
            for c in self.threads:
                c.join()
            sys.exit(0)


class Client(Thread):
    def __init__(self, client, address):
        Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            if data:
                data = data.decode('utf-8')
                request_header = data.split('\r\n')
                temp = request_header[0].split()
                if (len(temp) > 1):
                    request_file = temp[1]

                    if request_file == 'index.html' or request_file == '/' or request_file == '/index.html':
                        f = open('index.html', 'r')
                        response_data = f.read()
                        f.close()

                        content_length = len(response_data)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                          + str(content_length) + '\r\n\r\n'

                        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8') + b'\0')

                    elif request_file == 'dataset' or request_file == '/dataset':
                        files = []
                        for file in listdir('dataset'):
                            files.insert(len(files), '<p>' + file + '</p>')

                        response_data = '\r\n'.join(files)
                        content_length = len(response_data)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                          + str(content_length) + '\r\n\r\n'

                        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8') + b'\0')

                    elif 'dataset/' in request_file or '/dataset/' in request_file:
                        tempFile = request_file.split('/')
                        fileLoc = tempFile[len(tempFile) - 1]
                        if exists('dataset/' + fileLoc):
                            fileToRead = 'dataset/' + fileLoc
                            f = open(fileToRead, 'rb')
                            response_data = f.read()
                            f.close()
                            content_length = len(response_data)
                            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: multipart/form-data;\r\nContent-Length:' \
                                              + str(content_length) + '\r\n\r\n'

                            self.client.sendall(response_header.encode('utf-8') + response_data + b'\0')

                        else:
                            f = open('404.html', 'r')
                            response_data = f.read()
                            f.close()
                            content_length = len(response_data)
                            response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                              + str(content_length) + '\r\n\r\n'

                            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8') + b'\0')

                    else:
                        f = open('404.html', 'r')
                        response_data = f.read()
                        f.close()

                        content_length = len(response_data)
                        response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                          + str(content_length) + '\r\n\r\n'

                        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8') + b'\0')
            else:
                self.client.close()
                running = 0


if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.run()
