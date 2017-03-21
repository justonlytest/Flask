#coding=utf-8
from flask import Flask,render_template,redirect, make_response, flash
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter
from os import path
from .views import init_views

basedir = path.abspath(path.dirname(__file__))
nav = Nav()
bootstrap = Bootstrap()
db = SQLAlchemy()

class RegexConverter(BaseConverter):   #正则表达式类
    def __init__(self,url_map,*item):
        super(RegexConverter,self).__init__(url_map)
        self.regex = item[0]

def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    app.config.from_pyfile('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    # 与模版中的nav.top.render() 配合使用
    nav.register_element('top', Navbar(u'Flask入门', View(u'主页', 'index'), View(u'关于', 'about'), View(u'服务', 'services'),
                                       View(u'项目', 'project')))
    nav.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    init_views(app)
    return app


