#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import tornado.gen
import time

from common import user, tool


# 创建用户笔记
@tornado.gen.coroutine
def create(self, req_data):
    # print "create req_data:", req_data

    assert req_data.get("content"), "content cannot be empty"

    user_local_datetime = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime((req_data["ts"] / 1000)))

    record_content = {
        "content": req_data["content"],
        "width": req_data.get("width"),
        "height": req_data.get("height"),
    }

    record_content = tool.json_stringify(record_content)

    record_id = yield self.user.record.create(content=record_content, title=req_data["title"], content_type="note", create_datetime=user_local_datetime)

    self.user.log.create("CREATE_TEXT", record_id, user_local_datetime)

    raise tornado.gen.Return( "Note created succeed at %s." % user_local_datetime)


# 编辑用户笔记
@tornado.gen.coroutine
def edit(self, req_data):
    # print "edit req_data:", req_data

    assert req_data.get("id"), "id cannot be empty"
    assert req_data.get("content"), "content cannot be empty"

    user_local_datetime = time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime((req_data["ts"] / 1000)))

    record_content = {
        "content": req_data["content"],
        "width": req_data.get("width"),
        "height": req_data.get("height"),
    }

    record_content = tool.json_stringify(record_content)

    yield self.user.record.update(_id=req_data["id"], title=req_data["title"], content=record_content, update_datetime=user_local_datetime)

    self.user.log.create("SIGN_IN", req_data["id"], user_local_datetime)

    raise tornado.gen.Return( "Note editd succeed at %s." % user_local_datetime)


# 用户笔记列表
@tornado.gen.coroutine
def list(self, req_data):
    # print "list req_data:", req_data
    sort_by = {
        1: "title",
        2: "update_datetime",
        3: "create_datetime",
    }

    query = {
        "title": req_data.get("title") or None,
        "sortby": sort_by.get(abs(req_data["sort_type"])) or "title",
        "asc": req_data["sort_type"] > 0 and 1 or -1,
    }

    note_list = yield self.user.record.query_list(query, content_type="note")

    raise tornado.gen.Return(note_list)


# 查询笔记详情
@tornado.gen.coroutine
def query(self, req_data):
    # print "query req_data:", req_data

    note_detail = yield self.user.record.query(_id=req_data["id"])

    content = tool.json_load(note_detail["content"])
    note_detail["content"] = content["content"]
    note_detail["width"] = content["width"]
    note_detail["height"] = content["height"]

    raise tornado.gen.Return(note_detail)
