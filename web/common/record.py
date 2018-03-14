#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
""" record 类 """
import tornado.gen
from bson.objectid import ObjectId
import datetime

from common import tool, my_mongodb
import config

import user

class Record(object):

    def __init__(self, arg):
        super(Record, self).__init__()
        self.user = arg["user"]


    @tornado.gen.coroutine
    def create(self, title, content, content_type, create_datetime):
        content = self.user.encrypt_data(content)
        create_datetime = create_datetime or datetime.datetime.now()
        content_info = yield my_mongodb.MONGODBS["aypass"]["contents"].insert_one({
            "username": self.user.username,
            "title": title,
            "content_type": content_type or "text",
            "content": content,
            "create_datetime": create_datetime,
            "update_datetime": create_datetime,
        })

        raise tornado.gen.Return(content_info.inserted_id)


    @tornado.gen.coroutine
    def remove(self, _id):
        content_info = yield my_mongodb.MONGODBS["aypass"]["contents"].delete_one({
            "_id": ObjectId(_id),
        })

        raise tornado.gen.Return(content_info.raw_result)


    @tornado.gen.coroutine
    def query(self, _id):
        content_info = yield my_mongodb.MONGODBS["aypass"]["contents"].find_one({
            "_id": ObjectId(_id),
        })

        content_info["content"] = self.user.decrypt_data(content_info["content"])

        raise tornado.gen.Return(content_info)


    @tornado.gen.coroutine
    def query_list(self, query, content_type="text"):
        query_data = {
            "username": self.user.username,
            "content_type": content_type,
        }
        if query.get('title'):
            query_data['title'] = { "$regex": query['title'] }

        content_info = yield my_mongodb.MONGODBS["aypass"]["contents"].find(
            query_data,
            {
                "_id": 1,
                "title": 1,
                "update_datetime": 1,
                "create_datetime": 1,
            }
        ).sort([(query.get('sortby') or 'update_datetime', query.get('asc', -1))]).to_list(length=None)

        # print [(query.get('sortby') or 'update_datetime', query.get('asc', -1))]

        raise tornado.gen.Return(content_info)


    @tornado.gen.coroutine
    def query_all(self):
        content_info = yield my_mongodb.MONGODBS["aypass"]["contents"].find({
            "username": self.user.username,
        }).to_list(length=None)

        for item in content_info:
            item["content"] = self.user.decrypt_data(item["content"])

        raise tornado.gen.Return(content_info)


    @tornado.gen.coroutine
    def update(self, _id, title, content, update_datetime):
        content = self.user.encrypt_data(content)
        update_datetime = update_datetime or datetime.datetime.now()
        content_info = yield my_mongodb.MONGODBS["aypass"]["contents"].update_one({
            "_id": ObjectId(_id),
        }, {
            "$set":{
                "title": title,
                "content": content,
                "update_datetime": update_datetime,
            }
        })

        raise tornado.gen.Return(content_info.raw_result)


    @tornado.gen.coroutine
    def transfer_to_new_user(self, new_user):
        user_contents = yield my_mongodb.MONGODBS["aypass"]["contents"].find({
            "username": self.user.username,
        }).to_list(length=None)
        if user_contents:
            update_list = []
            for item in user_contents:
                item["content"] = content = self.user.decrypt_data(item["content"])
                item["content"] = new_user.encrypt_data(item["content"])
                item["username"] = new_user.username
                update_list.append(my_mongodb.MONGODBS["aypass"]["contents"].update_one({ "_id": item["_id"]}, {"$set": item}))

            result = yield update_list
        else:
            pass

        raise tornado.gen.Return(True)

