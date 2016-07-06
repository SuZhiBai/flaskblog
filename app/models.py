#_*_coding:utf-8_*_
from . import db,login_manager
from flask_login import UserMixin
from datetime import datetime
import bleach
from markdown import markdown


#class Role(db.Model):
#    __tablename__ ='roles'
#   id = db.Column(db.Integer,primary_key=True)
#    name = db.Column(db.String(60),nullable=True)
#    users = db.relationship('User',backref = 'role')


#子表的外键去关联主表的主键
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(60))
    #email = db.Column(db.String(60),nullable=True)
    password = db.Column(db.String(60))
    #role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    def __repr__(self):
        return '<Category %r>' % self.name
    def __unicode__(self):
        return self.name
class Post(db.Model):
    __tablename__= 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    fragment = db.Column(db.Text) #内容片段, 用于主页显示
    status = db.Column(db.Integer, default=1) #完成：1, 失败0, 草稿:-1  （暂时无用）
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())
    modified_time = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    view_count = db.Column(db.Integer, default=0)
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.fragment = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return '<Entry %r>' % self.title

    def __unicode__(self):
        return self.title

db.event.listen(Post.content, 'set', Post.on_changed_body)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
