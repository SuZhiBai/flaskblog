#-*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField(u'用户名',validators=[DataRequired()])
    password = PasswordField(u'密码',validators=[DataRequired()])
    submit = SubmitField(u'登陆')
