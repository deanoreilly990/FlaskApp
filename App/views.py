################################################
#  This script acts as the controller.
# It is the central control of the application
#
#

from flask import render_template, flash, redirect, session, url_for, request,session
from flask_login import login_user, logout_user, current_user, login_required
from App import app,handle,mysql
from flask import jsonify
import pandas as pd
import models

global year
global user
user = None
global sessionArea


@app.route('/') # If the application identifies there is no additional parameters after the url
def landing():
    # This function returns the landing page
    global year
    year = '2016'
    return render_template('landing.html')

# Handles the errors if they should arise
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')
@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html')
@app.errorhandler(502)
def page_not_found(e):
    return render_template('error.html')


@app.route('/index',methods=['POST']) ## Listens for a post request on the /index url
def index():
    global year
    global user
    global sessionArea
    sessionArea=request.form['Search'] # gathers the information from the posted object
    sessionArea.strip()
    crimes,mortage,area = models.overview(sessionArea) # Excutes the backend script
    if 'Not found' in crimes: # Checks for errors
        return render_template('error.html',error=crimes)
    else:
        return render_template('index1.html',crimes=crimes,mortage = mortage,area = area) # Passes data back to frontend

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
    if 'Not found:' in v1:
        return render_template('comparesearch.html',error = v1)
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
