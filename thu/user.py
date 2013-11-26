import os, os.path
import pickle
import getpass
from http.cookiejar import CookieJar
from urllib.request import Request, HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
from hashlib import md5
from collections import namedtuple
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

filename = os.path.join(os.environb[b'HOME'], b'.thu')

def _load(path = filename):
    with open(path, 'rb') as f:
        return pickle.load(f)

def _store(d, path = filename):
    with open(path, 'wb') as f:
        pickle.dump(d, f)
    os.chmod(path, 0o600)

BASE_URL = 'https://usereg.tsinghua.edu.cn/'

def checklogin(username, password):
    data = urlencode({
        'username': username,
        'password': md5(password).hexdigest(),
        'drop': 0,
        'type': 1,
        'n': 100
        })
    req = Request('http://net.tsinghua.edu.cn/cgi-bin/do_login', data.encode())
    resp = urlopen(req).read().decode()
    if(resp.startswith("password_error")):
        return "password error!" 
    elif(resp == "username_error"):
        return "username error!"
    else:
        return True

def setuser():
    username = input('Username: ').encode()
    password = getpass.getpass().encode()
    d = {}
    d['username'] = username
    d['password'] = password
    res = checklogin(username, password);
    if (res == True):
        _store(d)
        print("config ok.")
    else:
        print("Failed, " + res + "retry")

def show():
    print(_load())

def main():
    print(_load()['username'].decode())

try:
    _data = _load()
except Exception as e:
    print(e)
    setuser()
    _data = _load()

username = _data['username']
password = _data['password']
