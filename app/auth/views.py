#_*_coding:utf-8_*_
from flask import render_template,request,flash,url_for,make_response,redirect
from . import auth
from .forms import LoginForm
from ..models import User
from  .. import db
from flask_login import  login_user,logout_user,current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.username.data,password=form.password.data).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('main.index'))
    flash(u'用户名或密码错误，请重新输入')
    return render_template('login.html',title=u'登陆',form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))