import pymongo
import bcrypt
from flask_login import logout_user

import pprint
from flask import Flask,render_template,request,url_for, redirect, session
from flask_pymongo import PyMongo 

app = Flask(__name__)

app.secret_key = 'keynotknown'

client = pymongo.MongoClient(
    "mongodb+srv://whale-crawl:binomo123@cluster0.w1jbe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# get the database name
db = client.get_database('clustergr8')
# get the particular collection that contains the data
records = db.users

app.config['MONGO_URI'] =  "mongodb+srv://whale-crawl:binomo123@cluster0.w1jbe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

mongo = PyMongo(app)
db = client[ "myFirstDatabase" ]
col = db[ "fs.files" ]

mongo.send_file({'file':'send.py'})
