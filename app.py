from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "<marquee><h1>Hello, World</h1></marquee>"

@app.route("/userhome")
def userhome():
    return "<marquee><h1>USER HOME</h1></marquee>"

@app.route("/adminpanel")
def adminpanel():
    return "<marquee><h1>Admin Panel</h1></marquee>"