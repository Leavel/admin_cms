# _*_ coding:utf-8 _*_
import json
from flask import render_template, session, redirect, request, url_for
from app.admin import admin
from app.models import *
from app.api.api import admin_login,aes_decryption,aes_encryption


@admin.route('/')
def index():
    if "admin" in session:
        return render_template("admin/index.html")
    else:
        return render_template("admin/login.html")


@admin.route("/server-login",methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    print({"username":username,"password":password})
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


@admin.route('/server-logout',methods=["GET"])
def logout():
    print("text")
    session.pop("admin",None)
    return redirect("/admin")

