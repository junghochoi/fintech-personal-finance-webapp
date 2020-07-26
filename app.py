import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from datetime import datetime

import dummydata


app = Flask(__name__)
load_dotenv()

app.config['MONGO_DBNAME'] = 'ftf-final'
app.config['MONGO_URI'] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Login")

@app.route('/home')
def home():
    collection = mongo.db.posts
    posts = collection.find({}).sort('date')
    return render_template("homepage.html", posts=posts)

@app.route('/home/add-post', methods=["GET", "POST"])
def add_post():
    if request.method == "GET":
    
        return redirect(url_for("homepage.html"))
    else:
        posts = mongo.db.posts
        posts.insert({"post": request.form["post-message"], "category": request.form["post-category"]})
    
        return render_template("template.html", music=music)

@app.route('/analysis', methods=["GET"])
def analysis():

    # Some how get the list of transactions
    return render_template("analysis.html")







# AJAX Calls to server
@app.route("/analysis/balance")
def balance_info():
    # Replace this with some database stuff to get the user transactions.
    # User_transactions should look something similar to what is in dummydata
    # TODO: Discuss about database. Create Database.
    user_transactions = dummydata.transactions

    user_transactions.sort(key = lambda x : datetime.strptime(x["date"], "%Y/%m/%d"))

    return {
        "initialBalance": 300,
        "data": user_transactions    
    }


@app.route("/analysis/categories")
def categories_info():

    # we just need to return something like this 
    '''
    categories = {
        "eating out": 200,
        "car/transportation": 300,
        "housing": 4000,
        "entertainment": 10,
        "groceries": 80,
        "uncategorized": 1000
    }
    '''
    return dummydata.categories



    

