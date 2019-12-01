from functools import wraps
from ..models import *
from qiniu import Auth, put_stream, put_data

import geoip2.database
from flask import url_for
from app.admin.views import *
from Cryptodome.Cipher import AES
from Cryptodome import Random
from binascii import b2a_hex, a2b_hex
import requests

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
    mycipher = AES.new(key, AES.MODE_CFB, iv)
    password = iv + mycipher.encrypt(data.encode())

    return b2a_hex(password)


def aes_decryption(mysql_password, password):
    """
    密码解密
    :param mysql_password: 加密密码
    :param password: 解密密码
    :return:
    """
    mysql_password = a2b_hex(mysql_password)
    # print(mysql_password)
    mydecrrypt = AES.new(key, AES.MODE_CFB, mysql_password[:16])
    decrypttext = mydecrrypt.decrypt(mysql_password[16:]).decode()
    if str(decrypttext) == password:
        return True
    else:
        return False


def get_ip_info(ip):
    # 淘宝IP地址库接口
    r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip)
    if r.json()['code'] == 0:
        i = r.json()['data']
        # print(i)
        country = i["country"]  # 国家
        area = i["area"]  # 区域
        region = i["region"]  # 省份
        city = i["city"]  # 城市
        isp = i["isp"]  # 运营商
        country_id = i["country_id"]
        region_id = i["region_id"]
        return {"country": country, "area": area, "region": region, "city": city, "isp": isp}
    else:
        return None


def sensitive_word(word):
    """敏感词扫描"""
    sensitive = SensitiveWord.query().all()
    for item in sensitive.word:
        word = word.replace(item, '')
        return word


def qiniu_upload_file(source_file):
    """
    七牛云存储
    :param source_file:
    :return:
    """
    # 需要填写你的 Access Key 和 Secret Key
    access_key = "wZREIiDnElbkJeHZZuq2ahfsFwVYbw9NIwrLj-gx"
    secret_key = "WrG8CqIdyTTYt5R11Xg2OclLtrhCl2c_8qhIIl_F"
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = "leavel"
    domain_prefix = "file.7gongju.com"
    # 文件类型
    ALLOWED_EXT = ['png', 'jpg', 'jpeg', 'bmp', 'gif']

    if source_file.filename.find('.') > 0:
        file_ext = source_file.filename.rsplit('.', 1)[1].strip().lower()
        if file_ext in ALLOWED_EXT:
            save_file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext

            # 生成上传 Token，可以指定过期时间等
            token = q.upload_token(bucket_name, save_file_name)

            ret, info = put_data(token, save_file_name, source_file.stream)

            print(type(info.status_code), info)
            if info.status_code == 200:
                return domain_prefix + save_file_name
            return None
        return None
    return None
