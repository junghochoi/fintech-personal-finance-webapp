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
    if not session: 
        # return redirect(url_for('login'))
        return render_template("login.html")

    user_collection = mongo.db.users
    logged_in_username = session['username']
    user = user_collection.find_one({"username" : logged_in_username})

    net = user["currentBalance"]
    if net < 0:
        sign = "neg"
    else:
        sign = "pos"

    transaction_details = {
        "net": abs(net),
        "sign": sign,
        "earnings": user["totalEarnings"],
        "spending": user["totalSpending"]
    }

    posts_collection = mongo.db.posts
    posts = posts_collection.find({}).sort("date", -1)
    return render_template("homepage.html", trans=transaction_details, posts=posts, title="Home")

@app.route('/home/add-post', methods=["POST"])
def add_post():
    if not session:
        return redirect(url_for('index'))
   
    user_collection = mongo.db.users
    post_collection = mongo.db.posts

    logged_in_username = session['username']
    user = user_collection.find_one({"username" : logged_in_username})

    message = request.form["post-message"]
    category= request.form["post-category"]
    date = datetime.now()

    post = {
        "message" : message,
        "category" : category,
        "date" : date,
        "author" : logged_in_username
    }

    user["posts"].append(post)
    post_collection.insert(post)

    posts = post_collection.find({}).sort("date", -1)

    return redirect(url_for("home"))
    # return render_template("homepage.html", posts=posts)




@app.route('/transactions', methods=["GET"])
def transactions():
    if not session:
        return redirect(url_for('login'))

    user_collection = mongo.db.users
    user = user_collection.find_one({'username': session['username']})

    transactions = user["transactions"][::-1]
    print(transactions)
    return render_template("analysis.html", transactions=transactions)


@app.route('/transactions/add-transaction', methods=["POST"])
def add_transactions():

    if not session:
        redirect(url_for('login'))

    user_collection = mongo.db.users

    logged_in_username = session['username']
    user = user_collection.find_one({"username" :logged_in_username})

    title = request.form["trans-title"]
    amount = int(request.form["trans-amount"])
    details = request.form["trans-category"].split(",")
    main_category = details[0]
    spec_category = details[1]
    notes = request.form["trans-message"]
    date = datetime.now()

    if main_category == "spending":
        result = user["currentBalance"] - amount
        spendingUpdated = user["totalSpending"] + amount
        user_collection.update({'username': logged_in_username}, {'$set' : {'totalSpending': spendingUpdated}})
    else:
        result = user["currentBalance"] + amount
        earningsUpdated = user["totalEarnings"] + amount
        user_collection.update({'username': logged_in_username}, {'$set' : {'totalEarnings': earningsUpdated}})


    transaction = {
        "title": title,
        "amount": amount,
        "result": result,
        "main_category" : main_category,
        "spec_category": spec_category,
        "date" : date,
        "notes": notes
    }

    user_collection.update({'username' : logged_in_username}, {'$push' : {'transactions' : transaction}})
    user_collection.update({'username': logged_in_username}, {'$set' : {'currentBalance': result}})
    transactions = user["transactions"][::-1]

    return redirect(url_for("transactions"))
    # return render_template("analysis.html", transactions=transactions)
    # return redirect(f"https://0.0.0.0:5000{url_for('transactions')}")

@app.route('/learn', methods=["GET"])
def learn():
    return render_template("learning.html")




'''
    AUTHENTICATION ROUTES
'''

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form["username"]
        password = request.form["password"]

        collection = mongo.db.users
        user = list(collection.find({"username": username}))
        if len(user) == 0:
            collection.insert_one({
                "username": username, 
                "password": str(bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), 'utf-8'),
                "posts" : [],
                "transactions": [],
                "currentBalance" : 0,
                "totalSpending": 0,
                "totalEarnings": 0
            })
            session["username"] = username
            return redirect(url_for('home'))
            # return render_template("homepage.html")
        else:
            return render_template('signup.html', msg="Username already taken. Choose another one or login.")


@app.route("/login", methods= ["GET", "POST"])
def login():
    if session:
        # return redirect(url_for('home'))
        return render_template('analysis.html')
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
            return redirect(url_for('home'))
            # return render_template("homepage.html")
        else:
            return render_template('login.html', msg="Invalid password.")

@app.route('/logout', methods=["GET"]) 
def logout():
    session.clear()
    return redirect(url_for('index'))
    # return render_template("index.html")






# AJAX Calls to server
@app.route("/analysis/balance")
def balance_info():
    # Replace this with some database stuff to get the user transactions.
    # User_transactions should look something similar to what is in dummydata
    # TODO: Discuss about database. Create Database.

    user_collection = mongo.db.users
    user = user_collection.find_one({"username" : session['username']})



    # user_transactions = dummydata.transactions

    
    user_transactions = list(user['transactions'])
    # for x in user_transactions:
    #     print(x)


    # user_transactions.sort(key = lambda x : datetime.strptime(x["date"], "%Y/%m/%d"))
    user_transactions.sort(key = lambda x : x['date'])
    for t in user_transactions:
        t['date'] = t['date'].strftime("%m/%d/%y")
 
    
    return { "data": user_transactions}
    


@app.route("/analysis/categories")
def categories_info():

    # we just need to return something like this 


    user_collection = mongo.db.users
    user = user_collection.find_one({"username" : session['username']}) 


    user_transactions = list(user['transactions'])
    categories = {}

    for transaction in user_transactions:
        c = transaction['spec_category']
        t = int(transaction['amount'])
        if t > 0:
            continue
        else:
            t = -t


        if not c in categories.keys():
            categories[c] = t
        else:
            categories[c] += t
    



    return categories


    

