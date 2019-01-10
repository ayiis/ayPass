#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
""" user 类 """
import tornado.gen

from common import tool, mongodb
from handlers.dal import record, log


class User(object):

    def __init__(self, arg):
        super(User, self).__init__()
        self.key = tool.get_md5_digest(arg["username"])
        self.iv = tool.get_md5_digest(arg["password"])
        self.username = self.encrypt_data(arg["username"])
        self.password = self.encrypt_data(arg["password"])  # in fact, we dont need this
        self.logined = False
        self.userip = None
        self.user_info = None
        self.record = None
        self.log = None

    @tornado.gen.coroutine
    def login(self):

        # print "login:", self.username, self.password  # DEBUG
        user_info = yield mongodb.DBS["aypass"]["users"].find_one({
            "username": self.username,
            "password": self.password,
        })
        print("user_info:", user_info)  # DEBUG

        if user_info:
            self.user_info = user_info
            self.logined = True

            if self.logined is True:
                self.record = record.Record({"user": self})
                self.log = log.Log({"user": self})

        raise tornado.gen.Return(self.logined)

    def logout(self):
        self.logined = False
        self.user_info = None
        self.record = None
        return True

    @tornado.gen.coroutine
    def create(self):
        print("in exists")
        user_exists = yield mongodb.DBS["aypass"]["users"].count_documents({
            "username": self.username,
        })
        print("user_exists:", user_exists)
        if user_exists == 0:
            yield mongodb.DBS["aypass"]["users"].insert_one({
                "username": self.username,
                "password": self.password,
            })
            # print insert_result.inserted_id # DEBUG
            login = yield self.login()
            if login is True:
                raise tornado.gen.Return(True)

        raise Exception("User already exists")

    @tornado.gen.coroutine
    def __delete_user__(self):
        yield mongodb.DBS["aypass"]["users"].delete_one({
            "username": self.username,
        })

    @tornado.gen.coroutine
    def delete_user(self):
        yield mongodb.DBS["aypass"]["logs"].remove({
            "username": self.username,
        })
        yield mongodb.DBS["aypass"]["contents"].remove({
            "username": self.username,
        })
        yield self.__delete_user__()

        raise tornado.gen.Return(True)

    @tornado.gen.coroutine
    def change_password(self, old_password, new_username, new_password):

        assert self.logined is True, "Login required"
        # assert self.username == self.encrypt_data(new_username), "unmatched info" # 允许更改用户名
        assert self.password == self.encrypt_data(old_password), "unmatched info"

        new_user = User({"username": new_username, "password": new_password})
        result = yield new_user.create()
        if result is True:
            yield self.log.transfer_to_new_user(new_user)
            yield self.record.transfer_to_new_user(new_user)
            yield self.__delete_user__()
            self.logout()
            raise tornado.gen.Return(True)
        else:
            raise Exception("You fucked into another user.")

        # TODO: 通过修改 用户名+密码 合并两个用户的数据。
        # else:
        #     # raise tornado.gen.Return("Record already exists, create a new Password") # kidding me ?
        #     raise tornado.gen.Return("You've been fucking joined two Records")

    def encrypt_data(self, data):
        return tool.encrypt(data, self.key, self.iv)

    def decrypt_data(self, data):
        return tool.decrypt(data, self.key, self.iv)
