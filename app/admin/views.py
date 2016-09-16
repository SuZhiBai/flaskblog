#_*_coding:utf-8_*_
from flask import render_template,request,flash,url_for,make_response,redirect
from flask.ext.login import login_required,current_user
from . import admin
from .. import db
from ..models import User,Category,Post
from forms import UserForm,CategoryForm,PostForm
from datetime import datetime

'''
@admin.route('/console')
@login_required
def console():
    category_list = Category.query.all()
    return render_template('admin.html',category_list = category_list)
'''

#用户管理的增，删，改查
@admin.route('/listuser',methods=['GET','POST'])
@login_required
def listuser():
    user_list = User.query.all()
    category_list = Category.query.all()
    return render_template('listuser.html',title=u"用户列表",user_list=user_list,category_list = category_list)

@admin.route('/adduser',methods=['GET','POST'])
@login_required
def adduser():
    form = UserForm()
    if form.validate_on_submit():
        user = User(name=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.listuser'))
    return render_template('/adduser.html', form=form)

@admin.route('/edituser',methods=['GET','POST'])
@login_required
def edituser():
    form = UserForm()
    form.username.data = request.args.get('user_id')
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.listuser'))
    return render_template('/adduser.html', form=form)



@admin.route('/deluser',methods=['GET','POST'])
@login_required
def deluser():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.listuser'))

#栏目分类的增删改查
@admin.route('/listcategory',methods=['GET','POST'])
@login_required
def listcategory():
    category_list = Category.query.all()
    return render_template('listcategory.html',title=u'栏目列表',category_list=category_list)

@admin.route('/addcategory',methods=['GET','POST'])
@login_required
def addcategory():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data,)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin.listcategory'))
    return render_template('/addcategory.html', form=form)

@admin.route('/editcategory',methods=['GET','POST'])
@login_required
def editcategory():
    form = CategoryForm()
    form.name.data = request.args.get('category_id')
    if form.validate_on_submit():
        category = Category.query.filter_by(name=form.name.data).first()
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin.listcategory'))
    return render_template('/addcategory.html', form=form)



@admin.route('/delcategory',methods=['GET','POST'])
@login_required
def delcategory():
    category_id = request.args.get('category_id')
    category = User.query.filter_by(id=category_id).first()
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('admin.listcategory'))

@admin.route('/writepost', methods=['GET', 'POST'])
@login_required
def writepost():
    form = PostForm()
    category_list = Category.query.all()
    if form.validate_on_submit():
        post = Post(content=form.body.data,title=form.head.data,
                    category_id=form.category.data,
                    user_id=current_user._get_current_object().id)
       #内容、标题、作者、类别
        db.session.add(post)
        db.session.commit()
        flash(u"博客已发布")
        return redirect(url_for('main.index'))
    return render_template('writepost.html', form=form,category_list=category_list)

@admin.route('/editpost', methods=['GET', 'POST'])
@login_required
def editpost():
    post_list = Post.query.all()
    category_list = Category.query.all()
    return render_template('editpost.html',category_list = category_list,post_list=post_list)

@admin.route('/pushpost', methods=['GET', 'POST'])
@login_required
def pushpost():
    form = PostForm()
    category_list = Category.query.all()
    if request.args.get('post_id') and request.args.get('post_create_time') and request.args.get('post_title'):
        form_obj = Post.query.filter_by(id=request.args.get('post_id')).first()
        form.category.data = form_obj.category_id
        form.head.data = form_obj.title
        form.body.data = form_obj.fragment
        if form.validate_on_submit():
            form_obj.content = form.head.data
            form_obj.fragment = form.body.data
            form_obj.category_id = form.category.data
            print form_obj.category_id
            # 内容、标题、作者、类别
            db.session.add(form_obj)
            db.session.commit()
            return redirect(url_for('admin.editpost'))
    return render_template('writepost.html',category_list = category_list,form=form)

@admin.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@admin.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

