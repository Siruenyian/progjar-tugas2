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

# Read the config file in the server folder
config_object = ConfigParser()
config_object.read("./5025201080_5025201221_5025201248/server/httpserver.conf")
userinfo = config_object["Server"]
# print("port is {}".format(userinfo.get("port")))
