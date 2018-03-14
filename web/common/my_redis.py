#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
""" 初始化redis数据库 """
import redis, config

# 用 my_redis.REDISES["NAME"] 访问对应的 redis
REDISES = {}

class My_Redis(object):

    def __init__(self, arg):
        super(My_Redis, self).__init__()
        self.key_prefix = arg.get("key_prefix") or "BASE_API_COMMON_"

        try:
            self.rc = redis.Redis(connection_pool=redis.ConnectionPool(
                host=arg["host"],
                port=arg["port"],
                db=arg["db"],
                password=arg["passwd"],
                socket_connect_timeout=0.1,
                socket_timeout=0.1
            ))
        except Exception, e:
            print "Redis connection error:", str(e)
            raise

        for func_name in ["set", "get", "exists", "llen", "lpop", "lpush", "create_pipe", "ttl", "pipe_get", "pipe_set", "pipe_execute"]:
            self.wrapper(getattr(self, func_name), func_name)

        REDISES[arg["name"]] = self


    def wrapper(self, func, func_name):
        def do(*arga, **argb):
            try:
                return func(*arga, **argb)
            except Exception, e:
                print "Redis %s error: %s " % (func_name, str(e))
            return None
        return do

    def set(self, key, value, seconds=None):
        return self.rc.set(self.key_prefix + key, value, seconds)

    def get(self, key):
        return self.rc.get(self.key_prefix + key)

    def exists(self, key, seconds=None):
        return self.rc.exists(self.key_prefix + key)  # 存在返回1，不存在返回0

    def llen(self, key):
        return self.rc.llen(self.key_prefix + key)

    def lpop(self, key):
        return self.rc.lpop(self.key_prefix + key)

    def lpush(self, key, value):
        return self.rc.lpush(self.key_prefix + key,value)

    def create_pipe(self):
        # return self.rc.pipeline(transaction=False)
        return self.rc.pipeline()

    def ttl(self, key):
        return self.rc.ttl(self.key_prefix + key)

    def pipe_get(self, pipe, key):
        if not isinstance(pipe, redis.client.Pipeline):
            raise Exception("error@pipe_get->wrong type of pipe")
        pipe.get(self.key_prefix + key)

    def pipe_set(self, pipe, key, value, seconds):
        if not isinstance(pipe, redis.client.Pipeline):
            raise Exception("error@pipe_set->wrong type of pipe")
        pipe.set(self.key_prefix + key, value, seconds)

    def pipe_execute(self, pipe):
        if not isinstance(pipe, redis.client.Pipeline):
            raise Exception("error@pipe_execute->wrong type of pipe")
        return pipe.execute()


# 初始化所有数据库
def init():
    for item in config.REDIS:
        My_Redis({
            "name": item["NAME"],
            "host": item["HOST"],
            "port": item["PORT"],
            "db": item["DB"],
            "passwd": item["PASSWD"],
        })
        redis_client = REDISES[item["NAME"]]
        redis_client.set("aaaaaa", "123345", 1)
        assert redis_client.get("aaaaaa") == "123345", "REDIS %s inited FAILED!" % item["NAME"]
