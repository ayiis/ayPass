#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import json
import datetime
import re
import time
import decimal
import hashlib
import base64
import traceback
import zlib

from Crypto.Cipher import AES
from bson.objectid import ObjectId


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            if obj == datetime.datetime.min:
                return None
            else:
                return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            if obj == datetime.date.min:
                return None
            else:
                return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.timedelta):
            return time.strftime("%H:%M:%S", time.localtime(obj.seconds + 60 * 60 * (24 - 8)))  # hacked
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, bytes):
            return obj.decode("utf8")
        # elif isinstance(obj, enum.Enum):
        #     return obj.value
        elif isinstance(obj, Exception):
            return {
                "error": obj.__class__.__name__,
                "args": obj.args,
            }
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def wrap_unicode(data):
    if isinstance(data, dict):
        return {wrap_unicode(key): wrap_unicode(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [wrap_unicode(element) for element in data]
    elif isinstance(data, bytes):
        return data.decode("utf-8")
    else:
        return data


def json_stringify(data):
    return json.dumps(wrap_unicode(data), cls=MyEncoder)


def json_load(data):
    return wrap_unicode(json.loads(data))


def get_md5_digest(text, salt):
    text = "%s:%s" % (text, salt)
    text = text.encode("utf8")
    return hashlib.md5(text).digest()


class AESCipher(object):
    """
        Accept <unicode> and return <unicode>, or cannot count the right length
        afaik AES.MODE_CBC only accept utf8, AES.MODE_CFB may be another choice to handle Chinese
    """
    bs = 16

    @staticmethod
    def encrypt(raw_text, iv, key):
        raw_text = AESCipher._pad(raw_text)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(cipher.encrypt(raw_text))

    @staticmethod
    def decrypt(enc_text, iv, key):
        data = base64.b64decode(enc_text)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(data)
        decrypted = AESCipher._unpad(decrypted)
        return decrypted

    @staticmethod
    def _pad(text):
        t_len = len(text)
        if not isinstance(text, bytes):
            t_len = len(text.encode("utf8"))
        pan_len = AESCipher.bs - t_len % AESCipher.bs
        return text + pan_len * chr(pan_len)

    @staticmethod
    def _unpad(text):
        return text[:-ord(text[len(text) - 1:])]
