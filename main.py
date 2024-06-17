from flask import Flask, request, render_template, session, redirect, url_for
import requests, json
from datetime import datetime

# git add .
# git commit -m "my commit message"
# git push -u origin master


# flask --app main run

app = Flask(__name__)


# uvicorn main:app --reload
def load_mock_database():
    try:
        with open('database.json', 'r') as file:
            return json.load(file)
    except: 
        return {"error": "your database is blank"}

def is_authenticated(user_id):
    if user_id in ['test_user', 'jacob.good@sdi.com', 'richard_moser']:
        return True
    else:
        return False


@app.route('/', methods=['GET'])
def index():
    return render_template('pages/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    context = {}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print('login passowrd', password)

        if password == 'test_user':
            return redirect(url_for('get_results'))
        else:
            context = {"msg": "The username or password incorrect."}
            return render_template('pages/login.html', context=context)

    return render_template('pages/login.html',  context=context)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        dest = request.form['destination']
        items = request.form['items_to_buy']
        return redirect(url_for('get_results', destination=dest, items=items)) # pass the destination to the get_results page
    
    print(request.args.get('user_id'))
    auth = is_authenticated(request.args.get('user_id'))
    print('auth', auth)
    if auth == True:
        return render_template('pages/search.html')
    
    else:
        # if 
        return render_template('pages/login.html', context={})


@app.route('/imgoingresults', methods=['POST', 'GET'])
def get_results(destination=None, items=None):
    import random
    
    if destination != None:
        lat = round(random.uniform(40.0, 41.0), 4)
        long = round(random.uniform(76.0, 77.0), 4)
        what = random.choice(["apples", "bananas", "cherries", "water", "milk", "beer", "bread"])

    else: 
        lat = round(random.uniform(40.0, 41.0), 4)
        long = round(random.uniform(76.0, 77.0), 4)
        what = random.choice(["apples", "bananas", "cherries", "water", "milk", "beer", "bread"])

    all_data = load_mock_database()['data']
    print('loaded data')

    return_data = []

    for user in all_data:
        # match the likes
        if what in user['likes']:
            abs_long = abs(long - abs(user['long']))
            abs_lat = abs(lat - abs(user['lat']))

            if abs_long < 0.3 and abs_lat < 0.3:
                return_data.append(user)

    if len(return_data) == 0:
        context = {"message": "Sorry, no user has the same likes that is close to you."}

    else: 
        print('above all else')
        # First, sort by last_login in descending order
        sorted_by_login = sorted(return_data, key=lambda return_data: datetime.fromisoformat(return_data['last_login']), reverse=True)

        # Then, sort by the 'buy' status with 'False' entries at the top
        context = sorted(sorted_by_login, key=lambda x: x['buy_stuff']['buy'], reverse=True)
    
    # adjust the context to send back
    # Define the threshold date
    threshold_date = datetime.fromisoformat('2024-03-16T04:30:00')
    for entry in context:
        entry['logged_in_now'] = (datetime.fromisoformat(entry['last_login']) > threshold_date) and (entry['buy_stuff']['buy'] == True)

    # print(context)
    print('you have context')

    return render_template('pages/results.html', context=context)



