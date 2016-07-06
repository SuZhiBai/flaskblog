#-*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Required,EqualTo,Length
from flask.ext.pagedown.fields import PageDownField
from ..models import Category

class UserForm(Form):
    username = StringField(u'用户名',validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[Required() ,EqualTo('password2', message=u'密码必须相同.')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'提交')

class CategoryForm(Form):
    name = StringField(u'栏目名', validators=[DataRequired()])
    submit = SubmitField(u'提交')

class PostForm(Form):
    category = SelectField(u'文章类别', coerce=int)
    head = StringField(u'标题', validators=[Required(), Length(1, 25)])
    body = PageDownField(u"正文", validators=[Required()])
    submit = SubmitField(u'发布')
    def __init__(self, *args, **kwargs): #定义下拉选择表
        super(PostForm,self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                             for category in Category.query.order_by(Category.name).all()]