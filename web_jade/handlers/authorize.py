#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import re

from conf import config
from common import redisp

URL_SKIP_VALIDATE = set(["/login", "/api/user_login", "/api/user_create"])


# 验证请求内容之前，验证身份
def do(func):

    def wrap(self, *args, **kwargs):

        # 浏览器等不满足要求
        for allow_ua in config.SYSTEM["allow_ua"]:
            if re.match(allow_ua, self.request.headers.get("user-agent")) is not None:
                break
        else:
            print("ua:", self.request.headers.get("user-agent"))
            return self.render("deny")

        # 生产环境下，api接口是通过nginx转发访问的
        if config.SYSTEM["environment"] == "pro":
            # nginx 将<remote_ip>写入请求的 header["Ng-Real-Ip"] 中
            if self.request.remote_ip != "127.0.0.1" or not self.request.headers.get("Ng-Real-Ip"):
                return self.render("deny")

            self.request.remote_ip = self.request.headers.get("Ng-Real-Ip")

        access_code = self.get_secure_cookie("access_code")
        print("redisp.ONLINE_USERS:", redisp.ONLINE_USERS, access_code, self.request.uri)
        print("redisp.col", redisp.ONLINE_USERS.col)
        print("redisp.ONLINE_USERS.get(access_code):", redisp.ONLINE_USERS.get(access_code))
        # 无cookie且不在登录页
        if not access_code:
            if self.request.uri not in URL_SKIP_VALIDATE:
                return self.render("deny")
        # 有cookie但信息不在当前登录的用户列表
        elif not redisp.ONLINE_USERS.get(access_code):
            self.set_secure_cookie("access_code", "", expires=-1)
            return self.redirect("/login")

        user = redisp.ONLINE_USERS.get(access_code)
        if not user or not user.logined:
            if self.request.uri not in URL_SKIP_VALIDATE:
                raise Exception("User info have lost. Please relogin.")
        else:
            self.user = redisp.ONLINE_USERS.get(access_code)
            if self.user.userip != self.request.remote_ip:
                print(self.user.userip, " != ", self.request.remote_ip)
                raise Exception("User IP changed. Please relogin.")

        return func(self, *args, **kwargs)
    return wrap
