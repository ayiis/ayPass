#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import datetime

class MY_REDIS(object):
    col = {}
    key_timeout = 60 * 15
    def __init__(self, arg):
        super(MY_REDIS, self).__init__()
        ts = datetime.datetime.now()
        MY_REDIS.col = { key:{"ts": ts, "val": arg[key] } for key in arg }

    # todo, with tornado
    def cron_del_expire_user():
        pass

    def __getattr__(self, key):
        if not MY_REDIS.col.get(key):
            return None
        ts = datetime.datetime.now()
        if (ts - MY_REDIS.col[key]["ts"]).total_seconds() > MY_REDIS.key_timeout:
            del MY_REDIS.col[key]
            return None
        else:
            MY_REDIS.col[key]["ts"] = ts
            return MY_REDIS.col[key]["val"]

    def __setattr__(self, key, value):
        MY_REDIS.col[key] = {
            "val": value,
            "ts": datetime.datetime.now(),
        }

    def __setitem__(self, key, value):
        MY_REDIS.col[key] = {
            "val": value,
            "ts": datetime.datetime.now(),
        }

    def __delitem__(self, key):
        del MY_REDIS.col[key]

    def get(self, key):
        return self.__getattr__(key)


ONLINE_USERS = MY_REDIS({})


def init():
    from common import user

    ONLINE_USERS["q1WzY1aAHIK84suSs2Tq+w=="] = user.User({
        "username": "abc",
        "password": "123456",
    })

    ONLINE_USERS["L8bDmhfhBycOjcjtz9L2kA=="] = user.User({
        "username": "abc",
        "password": "123",
    })

    ONLINE_USERS["q1WzY1aAHIK84suSs2Tq+w=="].userip = "127.0.0.1"
    ONLINE_USERS["L8bDmhfhBycOjcjtz9L2kA=="].userip = "127.0.0.1"

    return [ONLINE_USERS["q1WzY1aAHIK84suSs2Tq+w=="].login(), ONLINE_USERS["L8bDmhfhBycOjcjtz9L2kA=="].login()]
