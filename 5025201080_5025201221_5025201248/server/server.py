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
config_object.read("./server/httpserver.conf")
userinfo = config_object["Server"]
print("port is {}".format(userinfo.get("port")))

response = urlopen('https://classroom.its.ac.id').read()
soup = BeautifulSoup(response)

print(soup.title.string)
print(soup.get_text())
