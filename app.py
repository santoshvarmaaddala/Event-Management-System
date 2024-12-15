from flask import Flask
from flask import render_template, request
from models import Event

app = Flask(__name__)
all_users = []  # My temp DataBase
all_events = []  # Events table


# Sample function to validate login credentials
def valid_login(username, password):
    # Hardcoded credentials for demonstration
    for user in all_users:
        if user['username'] == username and user['password'] == password:
            return user
    return None


def log_the_user_in(username):
    return f"Welcome, {username}!"


@app.route('/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        user = valid_login(request.form['username'], request.form['password'])
        if user:
            return render_template("admin.html", user=user)
        else:
            error = 'Invalid username/password'
    # Render the login form with error (if any)
    return render_template('login.html', error=error)


@app.route("/userhome")
def userhome():
    return render_template('userhome.html')


@app.route("/adminpanel")
def adminpanel():
    return render_template('admin.html', events=all_events)


# Manoj's Code


@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def adduser():
    username = request.form["username"]
    password = request.form["password"]
    for user in all_users:
        if user["username"] == username:
            print(user)
            return Exception("Username already exists try changing username")
    else:
        all_users.append(
            {
                "username": username,
                "password": password
            }
        )
        print(all_users[-1])

        return render_template("login.html", message="Please Login New User")


@app.route("/addevent", methods=['POST', 'GET'])
def add_events():
    if request.method == "GET":
        return render_template("eventsform.html")
    else:
        n_event = Event(request.form['eventname'],
                        request.form['capacity'],
                        request.form["location"],
                        request.form['pph'],
                        request.form['status'] == "True")

        all_events.append(n_event)

        return render_template("admin.html", events=all_events)
