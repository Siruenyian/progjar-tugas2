from bs4 import BeautifulSoup
from urllib.request import urlopen
import queue
from random import randint
import select
import socket
import sys
from threading import Thread
import bs4
from time import sleep
from html.parser import HTMLParser
from configparser import ConfigParser


config_object = ConfigParser()
config_object.read("./5025201080_5025201221_5025201248/server/httpserver.conf")
userinfo = config_object["Server"]
print("port is {}".format(userinfo.get("port")))
HOST = userinfo.get('host')
PORT = int(userinfo.get("port"))
# response = urlopen('https://classroom.its.ac.id').read()
# soup = BeautifulSoup(response)

# print(soup.title.string)
# print(soup.get_text())


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


if __name__ == "__main__":
    main()
