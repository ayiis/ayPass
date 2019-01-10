#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
""" record 类 """
import tornado.gen
import datetime

from common import mongodb

log_type = {
    "SIGN_IN": "",
    "SIGN_OUT": "",
    "SIGN_UP": "",
    "CREATE_TEXT": "",
    "CREATE_NOTE": "",
    "EDIT_TEXT": "",
    "EDIT_NOTE": "",
}


class Log(object):

    def __init__(self, arg):
        super(Log, self).__init__()
        self.user = arg["user"]

    @tornado.gen.coroutine
    def create(self, log_type, target, create_datetime):
        create_datetime = create_datetime or datetime.datetime.now()
        content_info = yield mongodb.DBS["aypass"]["logs"].insert_one({
            "username": self.user.username,
            "log_type": log_type,
            "target": target,
            "userip": self.user.userip,
            "create_datetime": create_datetime,
        })

        raise tornado.gen.Return(content_info.inserted_id)

    @tornado.gen.coroutine
    def query_list(self):
        content_info = yield mongodb.DBS["aypass"]["logs"].find({
            "username": self.user.username,
        }, {
            "_id": 0,
            "username": 0,
        }).sort([("create_datetime", -1)]).limit(50).to_list(length=None)

        raise tornado.gen.Return(content_info)

    @tornado.gen.coroutine
    def transfer_to_new_user(self, new_user):
        yield mongodb.DBS["aypass"]["logs"].update_many({"username": self.user.username}, {"$set": {"username": new_user.username}})

        raise tornado.gen.Return(True)
