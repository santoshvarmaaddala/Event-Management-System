from flask import Flask, url_for, redirect
from flask import render_template, request , session
from models import Event, User, BookEvent

app = Flask(__name__)
app.secret_key = "jhkgfjhkfgdjhkfgdjhfgdjhfgd"
all_users = []  # My temp DataBase
all_users.append(
    User(username="admin",password="1234",role="ADMIN")
)

all_events = []  # Events table
all_bookings = []

# Sample function to validate login credentials
def valid_login(username, password):
    # Hardcoded credentials for demonstration
    for user in all_users:
        if user.username == username and user.password == password:
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
            session['user'] = user.username
            session['role'] = user.role
            if user.role == "ADMIN":
                return render_template("admin.html", user=user, events=all_events)
            return render_template("userhome.html", user=user, events=all_events)
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
    role = request.form['role']
    for user in all_users:
        if user.username == username:
            print(user)
            return Exception("Username already exists try changing username")
    else:
        all_users.append(User(username, password))
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

@app.route("/book-event",methods=['POST'])
def b():
    username = session["user"]
    event = None
    for i in all_events:
        if i.event_name == request.form['event_name']:
            event = i
            break

    all_bookings.append(
        BookEvent(username , event)
    )
    # return redirect("userhome")
    return render_template("userhome.html",message="booking succesffull",events=all_events)

@app.route("/getall")
def getall():
    if session["role"] == "ADMIN":
        return render_template("bookings",books=all_bookings)
    temp = []
    for i in all_bookings:
        if i.username == session["user"]:
            temp.append(i)

    return render_template("bookings.html",books=temp)
@app.route("/createadmin")
def ca():
    return render_template("register.html", role="ADMIN")