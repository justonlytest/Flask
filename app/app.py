#coding=utf-8
from flask import Flask,render_template,redirect,request,make_response,url_for,abort,flash
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from os import path
app = Flask(__name__)
manager = Manager(app)
nav = Nav()
Bootstrap(app)

app.config.from_pyfile('config')
#与模版中的nav.top.render() 配合使用
nav.register_element('top',Navbar(u'Flask入门',View(u'主页','index'),View(u'关于','about'),View(u'服务','services'),View(u'项目','project')))
nav.init_app(app)

class RegexConverter(BaseConverter):   #正则表达式类
    def __init__(self,url_map,*item):
        super(RegexConverter,self).__init__(url_map)
        self.regex = item[0]
app.url_map.converters['regex'] = RegexConverter



@app.route('/')
def index():
    respone = make_response(render_template('index.html',title="Welcome"))
    respone.set_cookie('username','this is onlytest')
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


@app.route('/user/<regex("[a-z]{3}"):user_id>') #使用正则表达式
def user(user_id):
    return 'user %s' %user_id

@app.route('/login',methods=['GET','POST'])
def login():
    from Forms import LoginForm
    form = LoginForm()
    flash(u"登陆成功")
    return render_template('login.html',title=u"登陆",form=form)
@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath,'static/upload')
        f.save(upload_path,secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')



@manager.command
def dev():
    from livereload  import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404
if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)
