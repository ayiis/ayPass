import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../..")))

from common import tool

test_md5_salt = "1be66a30c78d41cf3c9ea0e794f5c746"

test_iv = tool.get_md5_digest("123456", test_md5_salt)
test_key = tool.get_md5_digest("13579", test_md5_salt)

test_text = "联系 我们123456text123410000"

# test_text = "1123456text"

enc_text = (tool.AESCipher.encrypt(test_text, test_iv, test_key))

print ("enc_text:", str(enc_text))

dec_text = tool.AESCipher.decrypt(enc_text, test_iv, test_key)

print ("dec_text:", dec_text)

