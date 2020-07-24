import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from datetime import datetime

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
    posts = collection.find({}).sort("date")
    return render_template("homepage.html", posts=posts)

@app.route('/home/add-post', methods=["GET", "POST"])
def add_post():
    if request.method == "GET":
        # return redirect(url_for("homepage.html"))
        return render_template("homepage.html")
    else:
        posts = mongo.db.posts
        posts.insert({ "date": datetime.now(), "post": request.form["post-message"], "category": request.form["post-category"] })
        posts = posts.find({}).sort("date")
        # return redirect(url_for("homepage.html"))
        return render_template("homepage.html", posts=posts)

@app.route('/analysis')
def analysis():
    return render_template("analysis.html")
