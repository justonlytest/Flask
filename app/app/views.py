#coding=utf-8
from flask import Flask,render_template,redirect, make_response, flash,request,url_for
from werkzeug.utils import secure_filename
from os import path
def init_views(app):
    @app.route('/')
    def index():
        respone = make_response(render_template('index.html', title="Welcome"))
        respone.set_cookie('username', 'this is onlytest')
        return respone

    @app.template_test('current_link')
    def current_link(link):
        return link == request.path

    @app.route('/services')
    def services():
        return 'Service'

    @app.route('/about')
    def about():
        return 'About'

    @app.route('/home')
    def home():
        return 'Home'

    @app.route('/project')
    def project():
        return 'project'

    @app.route('/user/<regex("[a-z]{3}"):user_id>')  # 使用正则表达式
    def user(user_id):
        return 'user %s' % user_id

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        from app.Forms import LoginForm
        form = LoginForm()
        flash(u"登陆成功")
        return render_template('login.html', title=u"登陆", form=form)

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == "POST":
            f = request.files['file']
            basepath = path.abspath(path.dirname(__file__))
            upload_path = path.join(basepath, 'static/upload')
            f.save(upload_path, secure_filename(f.filename))
            return redirect(url_for('upload'))
        return render_template('upload.html')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
