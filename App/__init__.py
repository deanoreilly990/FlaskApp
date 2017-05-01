from flask import Flask
from pymongo import MongoClient
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config.from_object('config')
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'USERS'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.secret_key = 'development key'

def connect():
# Substitute the 5 pieces of information you got when creating
# the Mongo DB Database (underlined in red in the screenshots)
# Obviously, do not store your password as plaintext in practice
    #connection = MongoClient('mongodb://dor:Abbie321@83.212.82.156:27017/HistData')
    connection = MongoClient('mongodb://localhost:27017/HistData')
    handle = connection["HistData"]
    return handle
handle=connect()


import os
from config import basedir
from App import views, models
