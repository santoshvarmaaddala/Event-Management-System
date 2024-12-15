from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('login.html')

@app.route("/userhome")
def userhome():
    return render_template('userhome.html')

@app.route("/adminpanel")
def adminpanel():
    return render_template('admin.html')