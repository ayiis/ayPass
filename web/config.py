#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import uuid

TORNADO_MAX_CLIENTS = 100

SYSTEM = {
    "api_port": 12356,
    "environment": "dev",
    "allow_ua": [
        r"^Mozilla/5.0 \(Macintosh; Intel Mac OS X 10_13_1*\) AppleWebKit/[0-9.]* \(KHTML, like Gecko\) Chrome/[0-9.]* Safari/[0-9.]*$",
        r"^Mozilla/5.0 \(Windows NT 6.1; Win64; x64\) AppleWebKit/[0-9.]* \(KHTML, like Gecko\) Chrome/[0-9.]* Safari/[0-9.]*$",
    ],
}

SECRET = {
    "md5_salt": "4670cd73e244522ca12072bf39e81aaa",
    "cookie_secret": uuid.uuid4().hex,
}

MONGODB={
    "aypass": {
        "HOSTS": "192.168.32.202",
        "HOST_PORT": 27017,
        "DATABASE_NAME": "my_world_star_bss_dev",
        "DATABASE_USER_NAME": "WORLD_STAR_BSS",
        "DATABASE_PASSWD": "WORLDSTAR001"
    }
}
