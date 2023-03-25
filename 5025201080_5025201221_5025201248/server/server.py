import queue
from random import randint
import select
import socket
import sys
from threading import Thread
from time import sleep
from configparser import ConfigParser

# Extra libraries for the first few numbers
import ssl
from bs4 import BeautifulSoup
import re


config_object = ConfigParser()
config_object.read("./5025201080_5025201221_5025201248/server/httpserver.conf")
userinfo = config_object["Server"]
print("port is {}".format(userinfo.get("port")))
HOST = userinfo.get('host')
PORT = int(userinfo.get("port"))


class ProcessThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.q = queue.Queue()

    def add(self, data):
        self.q.put(data)

    def stop(self):
        self.running = False

    def run(self):
        q = self.q
        while self.running:
            try:
                value = q.get(block=True, timeout=1)
                # Run stuff here
                process(value)
            except queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()

        if not q.empty():
            print("Elements left in the queue:")
            while not q.empty():
                print(q.get())


thread = ProcessThread()
thread.start()


def process(csock):
    data = csock.recv(4096).decode()
    # print(data)

    response = 'HTTP/1.1 200 OK\r\n\r\nHello World'
    csock.sendall(response.encode('utf-8'))
    # I am very confused why this needs closing but it works so I'm not complaining
    csock.close()


def main():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    print("Listening on port {p}...".format(p=PORT))

    server_socket.listen(5)
    while True:
        try:
            client_connection, client_address = server_socket.accept()
            read_ready, write_ready, exception = select.select(
                [client_connection, ], [], [], 2)
            if read_ready[0]:
                thread.add(client_connection)

        except KeyboardInterrupt:
            print("Stop.")
            break
        except socket.error:
            print("Socket error!")
            break
    cleanup()


def cleanup():
    thread.stop()
    thread.join()

# Method to formally request http protocol with socket


def connect(HOST):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, 443)
    client_socket.connect(server_address)
    # We have to warp this since it's a https(?)
    client_socket = ssl.wrap_socket(
        client_socket, ssl_version=ssl.PROTOCOL_SSLv23)
    request_header = 'GET / HTTP/1.1\r\nHost:{0}\r\n\r\n'.format(
        HOST)
    client_socket.send(request_header.encode())
    response = ''
    while True:
        received = client_socket.recv(1028)
        if not received:
            break
        response += received.decode('utf-8')
    client_socket.close()

    document = response.split('\r\n\r\n')
    headers = document[0]
    # in bytes
    htmldoc = document[1].encode()

    output = {}
    # Regex to sokit key value of headers
    result = re.findall(r"([\w-]+): (.*)\r", headers[1:])
    output = dict(result)
    if output["Content-Type"]:
        output["Content-Type"] = output["Content-Type"].split(' ')
    output["status"] = headers.split('\r\n')[0].split(" ", 1)
    return output, htmldoc


if __name__ == "__main__":
    headers, body = connect('www.its.ac.id')
    # print(headers)
    # 1. HTTP resp header
    print(headers["status"][1])
    # 2. content encoding
    # Still throws an error because if we pass a contenc encoding, the body will be ncoded
    # and I dont know how to decode it
    # print(headers["Content-Encoding"])
    # 3. HTTP version
    print(headers["status"][0])

    headers, body = connect('classroom.its.ac.id')
    # 4. Content type
    print(headers["Content-Type"][1])
    # 5.Parse
    # Doesnt work if number 2 is enabled
    soup = BeautifulSoup(body)
    print(soup.prettify())
    main()
