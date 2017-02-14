from flask import render_template, flash, redirect, session, url_for, request,session
from flask_login import login_user, logout_user, current_user, login_required
from App import app,handle,mysql
from .forms import LoginForm
from flask import jsonify
import pandas as pd
#from forms import ContactForm
from flask_mail import Message, Mail

mail = Mail()
global year
global user
user = None

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
    my_var = request.args.get('my_var', None)
    year = my_var
    return render_template('year.html',
                           year = my_var,user  = user )

@app.route('/search', methods=['POST'])
def search():
    global year
    global user
    datainfo = 'Cant Access Data '
    name=request.form['Search']
    name.strip()
    s = handle.PC.find({'Area':name},{'PC':1,'_id':0})
    if s:
        output = s[0]
        output = output['PC']
        output = str(output)
        output1 = '/static/images/History/'+str(year)+'/image1/Dublin_'+output+'.html?link=false"'
        output2 = '/static/images/History/'+str(year)+'/image2/Dublin_'+output+'.html?link=false"'
    else:
        output = "No such name"
    output = 'Dublin '+output
    if year == '2010':
        datainfo = handle.Data2010.find({'PostCode':output},{'Sum':1,'_id':0,'Min':1,'Max':1,'New Mean':1})
    elif year == '2011':
        datainfo = handle.Data2011.find({'PostCode':output},{'Sum':1,'_id':0,'Min':1,'Max':1,'New Mean':1})
    elif year == '2012':
        datainfo = handle.Data2012.find({'PostCode':output},{'Sum':1,'_id':0,'Min':1,'Max':1,'New Mean':1})
    elif year == '2013':
        datainfo = handle.Data2013.find({'PostCode':output},{'Sum':1,'_id':0,'Min':1,'Max':1,'New Mean':1})
    elif year == '2014':
        datainfo = handle.Data2014.find({'PostCode':output},{'Sum':1,'_id':0,'Min':1,'Max':1,'New Mean':1})
    elif year == '2015':
        datainfo = handle.Data2015.find({'PostCode':output},{'Sum':1,'_id':0,'Min':1,'Max':1,'New Mean':1})
    elif year == '2016':
        datainfo = handle.Data2016.find({'PostCode':output},{'Sum':1,'_id':0,'Min':1,'Max':1,'New Mean':1})

    info = datainfo[0]
    sumD = info['Sum']
    mean = info['New Mean']
    highest = info['Max']
    lowest = info['Min']






    return render_template('search.html', search = output1,image=output2,area=output,year=year,user  = user, sumData = sumD,mean = mean, max = highest,min=lowest)
