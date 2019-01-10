#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import tornado.gen

from handlers.dal import user
from common import redisp
import time


# 用户登录，@username, @password, @remember_me
@tornado.gen.coroutine
def login(self, req_data):
    # print "req_data:", req_data

    login_user = user.User({
        "username": req_data["username"],
        "password": req_data["password"],
    })

    login = yield login_user.login()
    if login is False:
        raise Exception("Access Denied")

    login_user.userip = self.request.remote_ip

    expires_days = req_data.get("remember_me") == "1" and 1 or None
    self.set_secure_cookie("access_code", login_user.username, expires_days=expires_days, HttpOnly=True)
    redisp.ONLINE_USERS[login_user.username] = login_user

    user_local_datetime = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime((req_data["ts"] / 1000)))
    login_user.log.create("SIGN_IN", "", user_local_datetime)

    raise tornado.gen.Return({"access_code": login_user.username})


# 用户退出
@tornado.gen.coroutine
def logout(self, req_data):
    del redisp.ONLINE_USERS[self.user.username]
    self.set_secure_cookie("access_code", "", expires_days=-1, HttpOnly=True)
    raise tornado.gen.Return(True)


# 更新用户密码
@tornado.gen.coroutine
def change(self, req_data):
    # print "req_data:", req_data
    success = yield self.user.change_password(req_data["old_password"], req_data["new_username"], req_data["new_password"])
    if success:
        del redisp.ONLINE_USERS[self.user.username]
        self.set_secure_cookie("access_code", "", expires_days=-1, HttpOnly=True)
        raise tornado.gen.Return(True)
    else:
        raise tornado.gen.Return(False)


# 用户注册
@tornado.gen.coroutine
def create(self, req_data):

    new_user = user.User({
        "username": req_data["username"],
        "password": req_data["password"],
    })

    login = yield new_user.login()
    if login is True:
        raise Exception("User already exists.")

    result = yield new_user.create()
    if result is True:
        login = yield new_user.login()
        if login is True:
            new_user.userip = self.request.remote_ip
            user_local_datetime = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime((req_data["ts"] / 1000)))
            new_user.log.create("SIGN_UP", "", user_local_datetime)
            raise tornado.gen.Return(True)

    raise tornado.gen.Return(False)


# 完全删除用户
@tornado.gen.coroutine
def delete(self, req_data):

    assert self.user.encrypt_data(req_data["username"]) == self.user.username, "User info do not match."
    assert self.user.encrypt_data(req_data["password"]) == self.user.password, "User info do not match."

    result = yield self.user.delete_user()
    if result is True:
        del redisp.ONLINE_USERS[self.user.username]
        self.set_secure_cookie("access_code", "", expires_days=-1, HttpOnly=True)
        raise tornado.gen.Return(True)
    else:
        raise Exception("Error")
