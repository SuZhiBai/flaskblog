#_*_coding:utf-8_*_
from flask import Flask,request
from werkzeug.routing import BaseConverter
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from flask.ext.pagedown import PageDown
#from .views import init_views

bootstrap = Bootstrap()
db= SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view='auth.login'

basedir = path.abspath(path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.txt')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/myflasky'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    from admin import admin as admin_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    #init_views(app)
    return app