#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import datetime
from common import tornado_timmer

class MY_REDIS(object):
    key_timeout = 6
    refresh_period = 30
    col = {}
    def __init__(self, arg):
        super(MY_REDIS, self).__init__()
        ts = datetime.datetime.now()
        MY_REDIS.col = { key:{"ts": ts, "val": arg[key] } for key in arg }
        tornado_timmer.set_interval(MY_REDIS.refresh_period, self.auto_refresh_expire_user)

    def auto_refresh_expire_user(self):
        ts = datetime.datetime.now()
        print MY_REDIS.col.items()
        MY_REDIS.col = { key: MY_REDIS.col[key] for key in MY_REDIS.col if (ts - MY_REDIS.col[key]["ts"]).total_seconds() < MY_REDIS.key_timeout }

    def __getattr__(self, key):
        return
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

    def __iter__(self) :
        return MY_REDIS.col.__iter__()

    def get(self, key):
        return
        return self.__getattr__(key)


ONLINE_USERS = MY_REDIS({})


ONLINE_USERS["aaaaaa"] = 123456

