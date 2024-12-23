from flask import Flask, render_template, request, session
from flask import redirect, url_for
from sqlalchemy import event

from models import db, Event, User, BookEvent


app = Flask(__name__)
app.secret_key = "jhkgfjhkfgdjhkfgdjhfgdjhfgd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


def valid_login(username, password):
    return User.query.filter_by(username=username, password=password).first()

@app.route('/')
def home():
    return render_template("index.html")

def is_logged_in():
    return 'user' in session

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        user = valid_login(request.form['username'], request.form['password'])
        if user:
            session['user'] = user.username
            session['role'] = user.role
            return redirect(url_for('landinghome'))
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    if "user" in session:
        session.clear()
    return redirect(url_for("login"))


@app.route('/home')
def landinghome():
    if not is_logged_in():
        return redirect(url_for('login'))
    user = session['user']
    if session["role"] == "ADMIN":
        events = Event.query.all()  
        return render_template("admin.html", user=user, events=events)
    events = Event.query.filter_by(status=True).all()
    return render_template("userhome.html", user=user, events=events)


@app.route('/register', methods=['GET'])
def register():
    ('Registered Successfully')
    return render_template("register.html", role="USER")


@app.route('/register', methods=['POST'])
def adduser():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form['role']
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "Username already exists, try changing the username"
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return render_template("login.html", message="Please Login New User")


@app.route("/addevent", methods=['POST', 'GET'])
def add_events():
    if not is_logged_in():
        return redirect(url_for('login'))
    if request.method == "GET":
        return render_template("eventsform.html")
    else:
        n_event = Event(
            event_name=request.form['eventname'],
            capacity=request.form['capacity'],
            location=request.form["location"],
            price_per_hour=request.form['pph'],
            status=request.form['status'] == "True"
        )
        db.session.add(n_event)
        db.session.commit()
        events = Event.query.all()
        return render_template("admin.html", events=events)


@app.route("/book-event", methods=['POST'])
def book_an_event():
    if not is_logged_in():
        return redirect(url_for('login'))
    username = session.get("user")  # Use .get() to handle missing session keys gracefully.
    if not username:
        return redirect(url_for('login'))  # Redirect to login if the user is not logged in.
    
    if session["role"] == "ADMIN":
        events = Event.query.all()  
        return render_template("admin.html")
    
    event_name = request.form.get('event_name')  # Use .get() to avoid KeyError if event_name is missing.
    if not event_name:
        return render_template("userhome.html", message="Event name is required.", events=Event.query.filter_by(status=True).all())

    # Fetch the event by name
    event = Event.query.filter_by(event_name=event_name, status=True).first()  # Ensure the event is not already booked (status = True).
    if not event:
        return render_template("userhome.html", message="Event not found or already booked.", events=Event.query.filter_by(status=True).all())

    # Mark the event as booked
    event.status = False
    db.session.add(event)

    # Add a new booking for the user
    new_booking = BookEvent(username=username, event_id=event.id)
    db.session.add(new_booking)

    # Commit all changes
    db.session.commit()

    # Fetch available events to display on the page
    events = Event.query.filter_by(status=True).all()
    return render_template("userhome.html", message="Booking successful.", events=events)

# function to convert id to eventname
def getName(id):
    event = Event.query.get(id)
    return event.event_name

def getIterable(iterable):
    res = []
    for item in iterable:
        res.append(
            {
                "user" : item.username,
                "event" : getName(item.event_id),
            }
        )

    return res

@app.route("/getall")
def getall():
    if not is_logged_in():
        return redirect(url_for('login'))
    if session["role"] == "ADMIN":
        bookings = BookEvent.query.all()
        bookings = getIterable(bookings)
        return render_template("bookings.html", books=bookings)
    user_bookings = BookEvent.query.filter_by(username=session["user"]).all()
    user_bookings = getIterable(user_bookings)
    return render_template("bookings.html", books=user_bookings)


@app.route("/createadmin")
def create_admin():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template("register.html", role="ADMIN")


with app.app_context():
    db.create_all()  # Create tables
    # Check if the default admin user exists
    admin_user = User.query.filter_by(username="admin").first()
    if not admin_user:
        # Add default admin user
        default_admin = User(username="admin", password="1234", role="ADMIN")
        db.session.add(default_admin)
        db.session.commit()
        print(db.session.query(User).all())
        print("Default admin user created: username='admin', password='1234'")
print("Database setup complete!")
app.run(debug=True)

# how to access event id from abouve url
@app.route('/delete/<int:event_id>',methods=['GET'])
def deleteevent(event_id):
    event = Event.query.get(event_id)
    print(event)
    if not event:
        return redirect(url_for("landinghome"))
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("landinghome"))
