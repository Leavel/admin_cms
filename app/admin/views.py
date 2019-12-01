# _*_ coding:utf-8 _*_
import json
import os
import uuid
from qiniu import Auth, put_stream, put_data
from flask import render_template, session, redirect, request, url_for
from sqlalchemy import func
import config
from app.admin import admin
from app.models import *
from app.api.api import admin_login, aes_decryption, aes_encryption, qiniu_upload_file


ALLOWED_EXT = ['png', 'jpg', 'jpeg', 'bmp', 'gif']


@admin.route('/')
def index():
    if "admin" in session:
        return render_template("admin/index.html")
    else:
        return render_template("admin/login.html")


@admin.route("/server-login", methods=["POST"])
def login():
    """登陆"""
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    # print({"username":username,"password":password})
    user = User.query.filter_by(user=username).first_or_404()
    if user:
        if aes_decryption(user.password, password) == True:
            session['admin'] = username
            dic = {
                "status": 1,
                "text": "True"
            }
        else:
            dic = {
                "status": 0,
                "text": "False"
            }
    else:
        dic = {
            "status": 0,
            "text": "uname does not exist"
        }
    return json.dumps(dic)


@admin.route('/server-logout', methods=["GET"])
def logout():
    """退出"""
    # print("text")
    session.pop("admin", None)
    return redirect("/admin")


@admin.route("/server-count-uv")
def server_count_uv():
    """地域分布数"""
    city = request.args.get('city', '')
    city_num = set(Traffic.query.filter_by(city=city).all())
    dic = {
        "count": len(city_num),
        "city": city
    }
    return json.dumps(dic)


@admin.route("/server-uv")
def server_uv_or_pv():
    """当月浏览量(uv/pv)"""
    date = request.args.get('date', '')
    data = Traffic.query.filter_by(date=date).all()
    uv = db.session.query(func.count(Traffic.id)).filter(Traffic.date == date).group("date").all()
    pv = db.session.query(func.sum(Traffic.pv)).filter(Traffic.date == date).group_by("date").all()
    dic = {
        "uv": uv,
        "pv": pv,
        "count": int(uv) + int(pv)
    }
    return json.dumps(dic)


@admin.route("/sensitive")
def sensitive():
    """敏感词"""
    word = request.args.get('sensitive_word','')
    sensitive = SensitiveWord(word=word)
    db.session.add(sensitive)
    db.session.commit()
    return render_template("admim/sensitive.html")



@admin.route('/file_upload/',methods=["POST"])
def upload():
    file=request.files['file']
    url = qiniu_upload_file(file)
    if url != None:
        db.session.add(Image(url=url))
        db.session.commit()

    return redirect('/profile/%d' % Image.id)
