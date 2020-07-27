import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from datetime import datetime
import dummydata
import bcrypt

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("KEY")

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
    posts = collection.find({}).sort("date", -1)
    return render_template("homepage.html", posts=posts, title="Home")

@app.route('/home/add-post', methods=["GET", "POST"])
def add_post():
    if request.method == "GET":
        # return redirect(url_for("homepage.html"))
        return render_template("homepage.html")
    else:
        posts = mongo.db.posts
        posts.insert({ "date": datetime.now(), "post": request.form["post-message"], "category": request.form["post-category"] })
        posts = posts.find({}).sort("date", -1)
        # return redirect(url_for("homepage.html"))
        return render_template("homepage.html", posts=posts)

@app.route('/transactions', methods=["GET"])
def analysis():

    # Some how get the list of transactions
    return render_template("analysis.html")


@app.route('/learn', methods=["GET"])
def learn():


    return render_template("learning.html")




'''
    AUTHENTICATION ROUTES
'''

@app.route("/signup", methods=["GET", "POST"])
def signup():
    session.clear()
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form["username"]
        password = request.form["password"]

        collection = mongo.db.users
        user = list(collection.find({"username": username}))
        if len(user) == 0:
            collection.insert_one({"username": username, "password": str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), 'utf-8')})
            session["username"] = username
            # return redirect(url_for('homepage'))
            return render_template("homepage.html")
        else:
            return render_template('signup.html', msg="Username already taken. Choose another one or login.")


@app.route("/login", methods= ["GET", "POST"])
def login():
    session.clear()
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form["username"]
        password = request.form["password"]

        collection = mongo.db.users
        user = list(collection.find({"username": username}))
        if len(user) == 0:
            return render_template('login.html', msg="Invalid username. Please create an account.")
        elif bcrypt.hashpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')) == user[0]['password'].encode('utf-8'):
            session["username"] = username
            # return redirect(url_for('homepage'))
            return render_template("homepage.html")
        else:
            return render_template('login.html', msg="Invalid password.")

@app.route('/logout', methods=["GET"]) 
def logout():
    session.clear()
    return render_template("index.html")






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



    

