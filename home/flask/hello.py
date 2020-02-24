from peeweetest import Classified
from view_form import UserForm

from datetime import datetime
from flask import Flask, render_template, Markup, url_for, session, request, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import jsonify
from werkzeug.utils import secure_filename
import os





app = Flask(__name__)

app.secret_key='SET_ME_BEFOE_BLA_BLA'

bootstrap = Bootstrap(app)
moment = Moment(app)
#test=Markup('<h2>just a test</h2>')
test='<h2>just a test</h2>'
#fortest=[1,2,3,4,5]
#session['login']='fail'

'''
@app.before_request
@app.route('/login', methods=['POST'])
def login():
    print
    if 'login'in session and session['login']=='leo':
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET'])
def login2():
    return render_template('login.html')
'''





@app.errorhandler(404)
def bad_req(error):
	return render_template('404.html'), 404


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    a=[sort.bicycle for sort in Classified.filter(person=99)]
    myit = iter(Classified.filter ( person = 99 ))

    return render_template('user.html',fortest=a, test=test, name=name, first='fff')



@app.route('/upload', methods=['POST', 'GET'])
def upload():
  if request.method == 'POST':
    f = request.files['file']
    basepath = os.path.dirname(__file__) # 當前檔案所在路徑
    upload_path = os.path.join(basepath, 'static/uploads',secure_filename(f.filename)) 
    f.save(upload_path)
    return redirect(url_for('upload'))
  return render_template('upload.html')

'''
@app.route('/write_session')
def writeSession():
    session['key_time']=datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    #return session['key_time']
    return str(session.modified)



@app.route('/read_session')
def  readSession():
    return session.get('key_time')
'''
@app.route('/form', methods=['GET', 'POST'])
def form2():
    #  flask_wtf類中提供判斷是否表單提交過來的method，不需要自行利用request.method來做判斷
    if request.method == 'POST':
        return 'Hello ' + request.values['username'] 
        #return None
        print('back get')
    #  如果不是提交過來的表單，就是GET，這時候就回傳user.html網頁
    return render_template('form.html')





@app.route('/url/arg')
def urlArg():
    return request.base_url
    #return request.args.get('next')








if __name__=='__main__':
	app.run(host='0.0.0.0')
        #app.run(host='0.0.0.0',port=80, debug=False)


