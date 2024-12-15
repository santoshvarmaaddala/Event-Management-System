from flask import Flask
from flask import render_template, request

app = Flask(__name__)


# Sample function to validate login credentials
def valid_login(username, password):
    # Hardcoded credentials for demonstration
    if username == "admin" and password == "12345":
        return True
    return False


def log_the_user_in(username):
    return f"Welcome, {username}!"


@app.route('/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # Render the login form with error (if any)
    return render_template('login.html', error=error)


@app.route("/userhome")
def userhome():
    return render_template('userhome.html')


@app.route("/adminpanel")
def adminpanel():
    return render_template('admin.html')


# Manoj's Code

all_users = []  # My temp DataBase


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

        return render_template("userhome.html",contextvars={
            "username": username
        })
