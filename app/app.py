#coding=utf-8
from flask import Flask,render_template,redirect,request,make_response,url_for,abort
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from flask_script import Manager
from os import path
app = Flask(__name__)
manager = Manager(app)
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


@app.route('/services')
def services():
    return 'Service'

@app.route('/about')
def about():
    return 'About'

@app.route('/project/')
def project():
    return 'project'


@app.route('/user/<regex("[a-z]{3}"):user_id>') #使用正则表达式
def user(user_id):
    return 'user %s' %user_id

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
    else:
        username = request.args['username']
    return render_template('login.html',method=request.method)

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath,'static/upload')
        f.save(upload_path,secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

@manager.command
def dev():
    from livereload  import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)

if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)
