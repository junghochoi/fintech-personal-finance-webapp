from datetime import datetime

transactions = [

    {
        "name": "fourth",
        "description": "I went out with a friend to eat pizza",
        "transaction": -20,
        "category"   : "Eating out",
        "date": "9/21/2020"

    },
    {
        "name": "Third",
        "description": "I went out with a friend to eat pizza",
        "transaction": -20,
        "category"   : "Eating out",
        "date": "7/22/2020"
    },
    {
        "name": "First",
        "description": "I went out with a friend to eat pizza",
        "transaction": -20,
        "category"   : "Eating out",
        "date": "7/20/2020"

    },
    {
        "name": "Second",
        "description": "I went out with a friend to eat pizza",
        "transaction": -20,
        "category"   : "Eating out",
        "date": "7/21/2020"

    },
    {
        "name": "fifth",
        "description": "I went out with a friend to eat pizza",
        "transaction": -20,
        "category"   : "Eating out",
        "date": "11/21/2020"

    },
    {
        "name": "zero",
        "description": "I went out with a friend to eat pizza",
        "transaction": -20,
        "category"   : "Eating out",
        "date": "1/21/2020"

    },
      {
        "name": "neagtive one",
        "description": "I went out with a friend to eat pizza",
        "transaction": -20,
        "category"   : "Eating out",
        "date": "1/21/2019"

    },

]

for t in transactions:
    print(t)
print("======")

transactions.sort(key = lambda x : datetime.strptime(x["date"], "%m/%d/%Y"))

for t in transactions:
    print(t)
