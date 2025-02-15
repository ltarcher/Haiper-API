# -*- coding:utf-8 -*-

import os
import time
from http.cookies import SimpleCookie
from threading import Thread

import requests

from utils import COMMON_HEADERS


class HaiperCookie:
    def __init__(self):
        self.cookie = SimpleCookie()
        self.session_id = None
        self.token = None

    def load_cookie(self, cookie_str):
        self.cookie.load(cookie_str)

    def get_cookie(self):
        return ";".join([f"{i}={self.cookie.get(i).value}" for i in self.cookie.keys()])

    def set_session_id(self, session_id):
        self.session_id = session_id

    def get_session_id(self):
        return self.session_id

    def get_token(self):
        return self.token

    def set_token(self, token: str):
        self.token = token


haiper_auth = HaiperCookie()
haiper_auth.set_session_id(os.getenv("SESSION_ID"))
#haiper_auth.load_cookie(os.getenv("ACCESS_TOKEN"))
haiper_auth.set_token(os.getenv("ACCESS_TOKEN"))

#打开F12，使用google登录，找到下面的请求：
#https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key=xxxxxxxxx
#获取key(Session_ID)、idToken以及refreshToken
#idToken可以不需要(如果同时使用浏览器,最好保持一致,否则浏览器会不可访问,token会被刷新)，refreshToken是必须的，后续可以保活


def update_token(haiper_cookie: HaiperCookie):
    headers = {}
    headers.update(COMMON_HEADERS)
    session_id = haiper_cookie.get_session_id()
    data = {"idToken": haiper_auth.get_token()}

    #定期调用google查询状态
    resp = requests.post(
        url=f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={session_id}",
        headers=headers,
        json=data,
        proxies={
            "http": os.getenv("PROXY_ADDRESS"),
            "https": os.getenv("PROXY_ADDRESS"),
        }  if int(os.getenv("USE_PROXY")) else None
    )

    resp_headers = dict(resp.headers)
    #print(resp_headers)
    err_resp = resp.json()

    #token过期，定期更新token

    if err_resp.get('error') and err_resp.get('error').get('code') == 400 and err_resp.get('error').get('message') == 'INVALID_ID_TOKEN':
        data = {
            "grant_type": "refresh_token",
            "refresh_token": os.getenv("REFRESH_TOKEN")
        }
        resp = requests.post(
            url=f"https://securetoken.googleapis.com/v1/token?key={session_id}",
            headers=headers,
            json=data,
            proxies={
                "http": os.getenv("PROXY_ADDRESS"),
                "https": os.getenv("PROXY_ADDRESS"),
            } if os.getenv("USE_PROXY") else None
        )
        token = resp.json().get("access_token")
        print("update token: {0}".format(token))
        haiper_cookie.set_token(token)

    # print(set_cookie)
    # print(f"*** token -> {token} ***")


def keep_alive(haiper_cookie: HaiperCookie):
    while True:
        try:
            update_token(haiper_cookie)
        except Exception as e:
            print(e)
        finally:
            time.sleep(5)


def start_keep_alive(haiper_cookie: HaiperCookie):
    t = Thread(target=keep_alive, args=(haiper_cookie,))
    t.start()


start_keep_alive(haiper_auth)
