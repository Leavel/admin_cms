# _*_ coding:utf-8 _*_
from flask import render_template,session,redirect,request
from app.admin import admin
from app.models import *
from app.api.api import admin_login,aes_decryption,aes_encryption


@admin.route('/')
def index():
    if "admin" in session:
        return render_template("admin/index.html")
    else:
        username = request.args.get("username","")
        password = request.args.get("password","")
        user = User.query.filter_by(user=username).first_or_404()
        if user:
            if aes_decryption(user.password,password):
                session['admin'] = username
                return render_template("admin/index.html")
            else:
                return "<script>alert('您输入的账号或密码错误')</script>"
        else:
            return "<script>alert('您输入的账号或密码错误')</script>"
        return render_template("admin/login.html")


