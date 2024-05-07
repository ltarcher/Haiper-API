# -*- coding:utf-8 -*-

from cookie import haiper_auth


def get_token():
    token = haiper_auth.get_token()
    try:
        yield token
    finally:
        pass
