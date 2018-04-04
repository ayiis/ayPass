#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import uuid

TORNADO_MAX_CLIENTS = 100

SYSTEM = {
    "api_port": 12356,      # 对外端口
    "environment": "dev",   # 生产环境改为 "pro"
    "allow_ua": [           # 匹配浏览器，允许以下的浏览器版本访问
        r"^Mozilla/5.0 \(Macintosh; Intel Mac OS X 10_13_1*\) AppleWebKit/[0-9.]* \(KHTML, like Gecko\) Chrome/[0-9.]* Safari/[0-9.]*$",
        r"^Mozilla/5.0 \(Windows NT 6.1; Win64; x64\) AppleWebKit/[0-9.]* \(KHTML, like Gecko\) Chrome/[0-9.]* Safari/[0-9.]*$",
    ],
}

SECRET = {
    "md5_salt": "4670cd73e244522ca12072bf39e81aaa",     # 用于md5加密，请务必更改
    "cookie_secret": uuid.uuid4().hex,                  # 一次性cookie加密因子，如果服务器重启，所有在线用户的cookie都会失效
}

MONGODB = {         # 用户数据保存到mongodb
    "aypass": {
        "HOSTS": "192.168.32.202",
        "HOST_PORT": 27017,
        "DATABASE_NAME": "my_world_star_bss_dev",
        "DATABASE_USER_NAME": "WORLD_STAR_BSS",
        "DATABASE_PASSWD": "WORLDSTAR001"
    }
}
