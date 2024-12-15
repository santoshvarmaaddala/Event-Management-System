from flask import Flask, render_template, request, session
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

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        user = valid_login(request.form['username'], request.form['password'])
        if user:
            session['user'] = user.username
            session['role'] = user.role
            if user.role == "ADMIN":
                events = Event.query.all()
                return render_template("admin.html", user=user, events=events)
            events = Event.query.all()
            return render_template("userhome.html", user=user, events=events)
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET'])
def register():
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
def b():
    username = session["user"]
    event_name = request.form['event_name']
    event = Event.query.filter_by(event_name=event_name).first()
    if event:
        new_booking = BookEvent(username=username, event_id=event.id)
        db.session.add(new_booking)
        db.session.commit()
    events = Event.query.all()
    return render_template("userhome.html", message="Booking successful", events=events)


@app.route("/getall")
def getall():
    if session["role"] == "ADMIN":
        bookings = BookEvent.query.all()
        return render_template("bookings.html", books=bookings)
    user_bookings = BookEvent.query.filter_by(username=session["user"]).all()
    return render_template("bookings.html", books=user_bookings)


@app.route("/createadmin")
def ca():
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