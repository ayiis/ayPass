#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
""" mongodb数据库连接 """
from motor.motor_tornado import MotorClient
import config

# 用 my_mongodb.MONGODBS["NAME"] 访问对应的 mongodb
MONGODBS = {}


def init():
    mongodbs = []
    for db_key in config.MONGODB:
        MONGODBS[db_key] = MotorClient(
            config.MONGODB[db_key]["HOSTS"],
            config.MONGODB[db_key]["HOST_PORT"]
        )[ config.MONGODB[db_key]["DATABASE_NAME"] ]

        mongodbs.append(
            MONGODBS[db_key].authenticate(
                config.MONGODB[db_key]["DATABASE_USER_NAME"],
                config.MONGODB[db_key]["DATABASE_PASSWD"]
            )
        )

    return mongodbs
