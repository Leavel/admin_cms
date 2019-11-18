# _*_ coding:utf-8 _*_
import json
from flask import render_template,session,redirect,request
from app.admin import admin
from app.models import *
from app.api.api import admin_login,aes_decryption,aes_encryption


@admin.route('/')
def index():
    if "admin" in session:
        return render_template("admin/index.html")
    else:
        return render_template("admin/login.html")


@admin.route("/server-login",methods=["GET"])
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    print({"username":username,"password":password})
    user = User.query.filter_by(user=username).first_or_404()
    if user:
        if aes_decryption(user.password, password) == True:
            session['admin'] = username
            dic = {
                "status": 1,
                "text": "uname already exist"
            }
        else:
            dic = {
                "status": 0,
                "text": "uname does not exist"
            }
    else:
        dic = {
            "status": 0,
            "text": "uname does not exist"
        }
    return json.dumps(dic)


