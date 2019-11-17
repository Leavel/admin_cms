from functools import wraps
from flask import url_for
from app.admin.views import *
from Cryptodome.Cipher import AES
from Cryptodome import Random
from binascii import b2a_hex,a2b_hex


key = b"qndisla19se35dlf"


def admin_login(f):
    """登陆装饰器"""
    @wraps(f)
    def decorate_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for(admin.admin))
        return f(*args, **kwargs)

    return decorate_function


def aes_encryption(password):
    """
    密码加密
    :param password: 需要加密的明文
    :return:
    """
    data = password
    iv = Random.new().read(AES.block_size)
    mycipher = AES.new(key,AES.MODE_CFB,iv)
    password = iv + mycipher.encrypt(data.encode())

    return b2a_hex(password)


def aes_decryption(mysql_password,password):
    """
    密码解密
    :param mysql_password: 加密密码
    :param password: 解密密码
    :return:
    """
    mysql_password = a2b_hex(mysql_password)
    print(mysql_password)
    mydecrrypt = AES.new(key,AES.MODE_CFB,mysql_password[:16])
    decrypttext = mydecrrypt.decrypt(mysql_password[16:]).decode()
    if str(decrypttext) == password:
        return True
    else:
        return False
