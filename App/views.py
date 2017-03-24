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


@app.route('/index',methods=['POST'])
def index():
    global year
    global user
    global sessionArea
    sessionArea=request.form['Search']
    sessionArea.strip()
    crimes = models.overview(sessionArea)
    return render_template('index1.html',crimes=crimes)

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

@app.route('/comparesearch', methods=['POST','GET'])
def comparesearch():
    global year
    return render_template('comparesearch.html',year=year)

@app.route('/result', methods=['POST'])
def result():
    global year
    compare1 =request.form['field1']
    compare2 =request.form['field2']
    value1= models.getDistanceInfo(compare1)
    value2 = models.getDistanceInfo(compare2)
    v1 = models.generateGraphs(compare1,compare2)
    return render_template('result.html',compare1=compare1,compare2=compare2,value1=value1,value2=value2,v1=v1)

@app.route('/home',methods=['GET'])
def home():
    crimes = models.genHome()
    return render_template('home.html', crimes=crimes)

@app.route('/search', methods=['POST'])
def search():
    global year
    global user
    global sessionArea
    datainfo = 'Cant Access Data '
    sessionArea=request.form['Search']
    sessionArea.strip()
    area, datainfo,location = models.gathersearch(sessionArea,year)
    try:
        info = datainfo[0]
        sumD = info['Sum']
        mean = info['New Mean']
        highest = info['Max']
        lowest = info['Min']
    except:
        error = datainfo[0]
        return render_template('year.html', error=error)

    return render_template('search.html',area=area,year=year,user  = user, sumData = sumD,mean = mean, max = highest,min=lowest,location = location)
@app.route('/story')
def story():
    return render_template('timeline.html')


from flask import request
from flask import jsonify

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200
