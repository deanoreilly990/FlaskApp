from flask import render_template, flash, redirect, session, url_for, request,session
from flask_login import login_user, logout_user, current_user, login_required
from App import app,handle,mysql
from .forms import LoginForm
from flask import jsonify
import pandas as pd
import models
#from forms import ContactForm
from flask_mail import Message, Mail

mail = Mail()
global year
global user
user = None
global sessionArea

#Route to handle User login
@app.route('/login', methods=['POST','GET'])
def login():
    global user
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
            user = username
            return redirect(url_for('index'))
    return render_template('login.html', error=error)
@app.route('/')
def landing():
    global year
    year = '2016'
    return render_template('landing.html')

@app.route('/index')
def index():
    global year
    global user
    year = '2016'
    return render_template('index.html',user=user)

@app.route('/logout')
def logout():
    global user
    user = None
    return redirect(url_for('index'))


@app.route('/year')
def year():
    global year
    global user
    global sessionArea
    my_var = request.args.get('my_var', None)
    year = my_var
    area, datainfo,location = models.gathersearch(sessionArea,year)
    info = datainfo[0]
    sumD = info['Sum']
    mean = info['New Mean']
    highest = info['Max']
    lowest = info['Min']
    return render_template('search.html',area=area,year=year,user  = user, sumData = sumD,mean = mean, max = highest,min=lowest,location = location)


@app.route('/search', methods=['POST'])
def search():
    global year
    global user
    global sessionArea
    datainfo = 'Cant Access Data '
    sessionArea=request.form['Search']
    sessionArea.strip()
    area, datainfo,location = models.gathersearch(sessionArea,year)
    #error = datainfo
    #return render_template('year.html', error=error)
    info = datainfo[0]
    sumD = info['Sum']
    mean = info['New Mean']
    highest = info['Max']
    lowest = info['Min']

    return render_template('search.html',area=area,year=year,user  = user, sumData = sumD,mean = mean, max = highest,min=lowest,location = location)
