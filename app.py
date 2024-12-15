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

@app.route('/login', methods=['POST', 'GET'])
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