#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import tornado.gen
import time

from common import user, tool


# 用户笔记列表
@tornado.gen.coroutine
def list(self, req_data):
    # print "list req_data:", req_data

    log_list = yield self.user.log.query_list()

    raise tornado.gen.Return(log_list)

