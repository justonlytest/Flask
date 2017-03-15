#coding=utf-8
from flask import Flask,render_template,redirect,request
from werkzeug.routing import BaseConverter
app = Flask(__name__)

class RegexConverter(BaseConverter):   #正则表达式类
    def __init__(self,url_map,*item):
        super(RegexConverter,self).__init__(url_map)
        self.regex = item[0]
app.url_map.converters['regex'] = RegexConverter


@app.route('/')
def index():
    return render_template('index.html',title="Welcome")

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
    return render_template('login.html',method=request.method)

if __name__ == '__main__':
    app.run()
