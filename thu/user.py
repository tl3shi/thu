import os, os.path
import pickle
import getpass
from http.cookiejar import CookieJar
from urllib.request import Request, HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
from hashlib import md5
from collections import namedtuple
from bs4 import BeautifulSoup


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
    cj = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cj))
    password = md5(password).hexdigest()
    url = BASE_URL + 'do.php'
    data = dict(
            action = 'login',
            user_login_name = username,
            user_password = password
            )
    req = Request(url, urlencode(data).encode('utf8'))
    resp = opener.open(req)
    content = resp.read().decode('gbk')
    if content != 'ok':
        print(content)
        return False
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
        print("Failed, retry")

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
