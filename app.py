import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from datetime import date, datetime
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




@app.route('/transactions/<timeframe>', methods=["GET"])
def transactions(timeframe="total"):
    if not session:
        return redirect(url_for('login'))

    user_collection = mongo.db.users
    user = user_collection.find_one({'username': session['username']})

    all_transactions = user["transactions"][::-1]
    transactions = []
    
    if timeframe == "year":
        for trans in all_transactions:
            old_date_arr = current_date.split("-")
            old_date = str(int(old_date_arr[0]) - 1) + "-" + old_date_arr[1] + "-" + old_date_arr[2]
            if trans["date"].split(" ") >= old_date:
                transactions += trans
    elif timeframe == "month":
        for trans in all_transactions:
            old_date_arr = current_date.split("-")
            old_date = old_date_arr[0] + "-" + str(int(old_date_arr[1]) - 1) + "-" + old_date_arr[2]
            if trans["date"].split(" ") >= old_date:
                transactions += trans
    elif timeframe == "day":
        for trans in all_transactions:
            old_date_arr = current_date.split("-")
            old_date = old_date_arr[0] + "-" + old_date_arr[1] + "-" + str(int(old_date_arr[2]) - 1)
            if trans["date"].split(" ") >= old_date:
                transactions += trans
    else:
        transactions = all_transactions

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


    # user_collection.update({'username' : logged_in_username}, {'$push' : {'transactions' : transaction}})
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



@app.route("/analysis/specify")
def reroute_timeframe():
    timeframe = request.form["timeframe"]
    if timeframe == "Year":
        change_timeframe("year")
        return redirect(url_for("/transactions/year"))
    elif timeframe == "Month":
        change_timeframe("month")
        return redirect(url_for("/transactions/month"))
    elif timeframe == "Day":
        change_timeframe("day")
        return redirect(url_for("/transactions/day"))
    else:
        change_timeframe()
        return redirect(url_for("transactions/total"))


# AJAX Calls to server


@app.route("/analysis/<timeframe>")
def change_timeframe(timeframe="total"):
    user_collection = mongo.db.users
    user = user_collection.find_one({"username" : session['username']})    


    # Balances Data
    all_transactions = list(user['transactions'])

    current_date = date.today()
    user_transactions = []

    if timeframe == "year":
        for trans in all_transactions:
            old_date_arr = current_date.split("-")
            old_date = str(int(old_date_arr[0]) - 1) + "-" + old_date_arr[1] + "-" + old_date_arr[2]
            if trans["date"].split(" ") >= old_date:
                user_transactions += trans
    elif timeframe == "month":
        for trans in all_transactions:
            old_date_arr = current_date.split("-")
            old_date = old_date_arr[0] + "-" + str(int(old_date_arr[1]) - 1) + "-" + old_date_arr[2]
            if trans["date"].split(" ") >= old_date:
                user_transactions += trans
    elif timeframe == "day":
        for trans in all_transactions:
            old_date_arr = current_date.split("-")
            old_date = old_date_arr[0] + "-" + old_date_arr[1] + "-" + str(int(old_date_arr[2]) - 1)
            if trans["date"].split(" ") >= old_date:
                user_transactions += trans
    else:
        user_transactions = all_transactions

    user_transactions.sort(key = lambda x : x['date'])
    for t in user_transactions:
        t['date'] = t['date'].strftime("%m/%d/%y")


    # Categories Data and income-expenses
    categories = {}
    for transaction in user_transactions:
        if  transaction['main_category'] == 'earnings':
            continue
        c = transaction['spec_category']
        t = int(transaction['amount'])

        if not c in categories.keys():
            categories[c] = t
        else:
            categories[c] += t
    return categories

    # income-expenses data


 
    
    return { 
        "balance": user_transactions,
        "categories" : categories,
        
    }



@app.route("/analysis/balance")
def balance_info():
    user_collection = mongo.db.users
    user = user_collection.find_one({"username" : session['username']})    
    user_transactions = list(user['transactions'])
    user_transactions.sort(key = lambda x : x['date'])


     
    for t in user_transactions:
        t['date'] = t['date'].strftime("%m/%d/%y")
 
    
    return { "data": user_transactions}
    


@app.route("/analysis/categories")
def categories_info():
    user_collection = mongo.db.users
    user = user_collection.find_one({"username" : session['username']}) 


    user_transactions = list(user['transactions'])
    categories = {}

    for transaction in user_transactions:
        if  transaction['main_category'] == 'earnings':
            continue
        c = transaction['spec_category']
        t = int(transaction['amount'])

        if not c in categories.keys():
            categories[c] = t
        else:
            categories[c] += t
    return categories

@app.route('/analysis/income-expenses')
def income_expenses_info():
    pass
    



    

