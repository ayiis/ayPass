#AES-demo

import base64
from Crypto.Cipher import AES

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../..")))

from common import tool

test_md5_salt = "1be66a30c78d41cf3c9ea0e794f5c746"

test_iv = tool.get_md5_digest("123456", test_md5_salt)
test_key = tool.get_md5_digest("13579", test_md5_salt)

test_text = "联系 我们123456text"


'''
采用AES对称加密算法
'''
# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes
#加密方法
def encrypt_oracle():
    # 秘钥
    key = '123456'
    # 待加密文本
    mystr = '人生苦短，py是岸'
    text = base64.b64encode(mystr.encode('utf-8')).decode('ascii')
    # 初始化加密器
    aes = AES.new(test_key, AES.MODE_CBC, test_iv)
    #先进行aes加密
    zzz = add_to_16(test_text)
    encrypt_aes = aes.encrypt(zzz)
    #用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    print(encrypted_text)

#解密方法
def decrypt_oralce():
    # 秘钥
    key = '123456'
    # 密文
    text = 'ofyYz83X2RP0QeGYQH3JrU1rd7NLlN4LJSS9F6iOD/E='
    # 初始化加密器
    aes = AES.new(test_key, AES.MODE_CBC, test_iv)
    #优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    #
    decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8') # 执行解密密并转码返回str
    decrypted_text = base64.b64decode(decrypted_text.encode('utf-8')).decode('utf-8')
    print(decrypted_text)

if __name__ == '__main__':
   encrypt_oracle()
   decrypt_oralce()
