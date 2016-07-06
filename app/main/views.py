#_*_coding:utf-8_*_
from flask import render_template,request,flash,url_for,make_response,redirect
from flask.ext.login import login_required
from . import main
from ..models import User,Category,Post
from datetime import datetime

#def init_views(app):
@main.route('/')
def index():
    category_list = Category.query.all()
    #posts=Post.query.order_by(Post.create_time.desc()).all()
    page_index = request.args.get('page',1,type=int)
    query = Post.query.order_by(Post.create_time.desc())
    #将参数传给对象模型的分页方法，得到分页数据
    pagination = query.paginate(page_index,per_page=2,error_out=False)
    posts = pagination.items
    return render_template('index.html',category_list = category_list,posts=posts,pagination=pagination)

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500