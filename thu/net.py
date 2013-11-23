__all__ = ['check', 'login', 'logout', 'main']

from urllib.request import urlopen, Request
from urllib.parse import urlencode
from hashlib import md5
from collections import namedtuple

from .user import username, password

NetUsage = namedtuple('NetUsage', 'id user traffic unknown timelen')

response_code_map = {"user_tab_error": "认证程序未启动",
"user_group_error": "您的计费组信息不正确",
"non_auth_error": "您无须认证，可直接上网",
"status_error": "用户已欠费，请尽快充值。",
"available_error": "您的帐号已停用",
"delete_error": "您的帐号已删除",
"ip_exist_error": "IP已存在，请稍后再试。",
"usernum_error": "用户数已达上限",
"online_num_error": "该帐号的登录人数已超过限额\n" +
    "请登录https://usereg.tsinghua.edu.cn断开不用的连接。",
"mode_error": "系统已禁止WEB方式登录，请使用客户端",
"time_policy_error": "当前时段不允许连接",
"flux_error": "您的流量已超支",
"minutes_error": "您的时长已超支",
"ip_error": "您的 IP 地址不合法",
"mac_error": "您的 MAC 地址不合法",
"sync_error": "您的资料已修改，正在等待同步，请 2 分钟后再试。",
"ip_alloc": "您不是这个地址的合法拥有者，IP 地址已经分配给其它用户。",
"ip_invaild": "您是区内地址，无法使用。"
        }

def check():
    req = Request('http://net.tsinghua.edu.cn/cgi-bin/do_login', b'action=check_online')
    resp = urlopen(req).read().decode()
    info = NetUsage(*resp.split(','))
    print(info)

def login():
    data = urlencode({
        'username': username,
        'password': md5(password).hexdigest(),
        'drop': 0,
        'type': 1,
        'n': 100
        })
    req = Request('http://net.tsinghua.edu.cn/cgi-bin/do_login', data.encode())
    resp = urlopen(req).read().decode()
    if(resp in response_code_map.keys()):
        print(response_code_map[resp])
        exit(0)
    check()

def logout():
    req = Request('http://net.tsinghua.edu.cn/cgi-bin/do_logout', b'')
    print(urlopen(req).read().decode())

main = check
