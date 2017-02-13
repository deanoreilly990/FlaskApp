from flask import render_template, flash, redirect, session, url_for, request,session
from flask_login import login_user, logout_user, current_user, login_required
from App import app,handle,mysql
from .forms import LoginForm
from flask import jsonify
#from forms import ContactForm
from flask_mail import Message, Mail

mail = Mail()
global year

#Route to handle User login
@app.route('/login', methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * from User where UserNAME='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)
@app.route('/')
@app.route('/index')
def index():
    global year
    year = 2016
    return render_template('index.html')
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/year')
def year():
    global year
    my_var = request.args.get('my_var', None)
    year = my_var
    return render_template('year.html',
                           year = my_var)

@app.route('/search', methods=['POST'])
def search():
    global year
    name=request.form['Search']
    name.strip()
    s = handle.PC.find({'Area':name},{'PC':1,'_id':0})
    if s:
        output = s[0]
        output = output['PC']
        output1 = '/static/images/History/'+str(year)+'/image1/Dublin_'+str(output)+'.html?link=false"'
        output2 = '/static/images/History/'+str(year)+'/image2/Dublin_'+str(output)+'.html?link=false"'
    else:
        output = "No such name"
    return render_template('search.html', search = output1,image=output2,area=output,year = year)
