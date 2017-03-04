from flask import render_template, flash, redirect, session, url_for, request,session
from flask_login import login_user, logout_user, current_user, login_required
from App import app,handle,mysql
from .forms import LoginForm
from flask_script import Manager
from flask import jsonify
import pandas as pd
import models
import googlemaps
from datetime import datetime
import CurrentSchool
#from forms import ContactForm
from flask_mail import Message, Mail

def gathersearch(name,year):
    sessionArea = handle.PC.find({'Area':name},{'PC':1,'_id':0})
    try:
        if sessionArea:
            output = sessionArea[0]
            output = output['PC']
            output = str(output)
            area = output
    except:
        error = 'Not found: Ensure in Dublin, Check spelling'
        return render_template('year.html', error=error)
    output = 'Dublin '+output
    datainfo = 'empty'+ str(name) + str(year)
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

    location = 'null'

    fingal = ['11','13','15','17','NCD']
    DC =['1','3','7','8','9','2','10']
    SD =['12','20','22','24','D6w','WCD']
    DLR =['4','6','14','16','18','Dun Laoghaire Rathdown']
    if area in fingal:
        location ='Fingal'
    elif area in SD:
        location = 'South Dublin'
    elif area in DC:
        location = 'Dublin City'
    elif area in DLR:
        location = 'DLR'
    return area,datainfo,location

def getDistanceInfo(value1,value2):
    now = datetime.now()
    gmaps = googlemaps.Client(key='AIzaSyA6Ie_h7a_Qgl0vT1IEFrf3qeHMtGg_5cs')
    directions_results = gmaps.directions(value1,"Dublin City Centre,Ireland",mode="driving",departure_time=now)
    keys = directions_results[0].keys()
    key = directions_results[0][keys[6]][0].keys()
    time = directions_results[0][keys[6]][0][key[8]][u'text']
    time = time.encode('ascii','ignore')
    dist = directions_results[0][keys[6]][0][key[0]][u'text']
    dist = dist.encode('ascii','ignore')
    value1 = [time,dist]
    now = datetime.now()
    gmaps = googlemaps.Client(key='AIzaSyA6Ie_h7a_Qgl0vT1IEFrf3qeHMtGg_5cs')
    directions_results = gmaps.directions(value2,"Dublin City Centre,Ireland",mode="driving",departure_time=now)
    keys = directions_results[0].keys()
    key = directions_results[0][keys[6]][0].keys()
    time = directions_results[0][keys[6]][0][key[8]][u'text']
    time = time.encode('ascii','ignore')
    dist = directions_results[0][keys[6]][0][key[0]][u'text']
    dist = dist.encode('ascii','ignore')
    value2 = [time,dist]
    return value1,value2

def generateGraphs(value1,value2):
    #logd = Manager(logdata)
    v1 = handle.PC.find({'Area':value1},{'PC':1,'_id':0})
    v2 = handle.PC.find({'Area':value2},{'PC':1,'_id':0})
    try:
        if v1:
            output = v1[0]
            output = output['PC']
            output = str(output)
            v1 = 'dublin '+str(output)
        if v2:
            output = v2[0]
            output = output['PC']
            output = str(output)
            v2 ='dublin '+str(output)
    except:
        error = 'Not found: Ensure in Dublin, Check spelling'
        return render_template('comparesearch.html', error=error)
    v1,v2 = CurrentSchool.logdata(v1,v2)
    return v1,v2
