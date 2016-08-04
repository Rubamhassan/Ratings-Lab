"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Rating, Movie, connect_to_db, db)


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/register', methods=["GET"])
def register():
    """ take us to register_form page"""

    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_form():
    """ take us to register_form page"""

    emailaddress= request.form.get('emailaddress')
    password= request.form.get('password')

    user=User.query.filter_by(email=emailaddress).first()
    if user==None:
        user = User(email=emailaddress,
                    password=password)
        #We may need to move line 47 one tab to the left
        db.session.add(user)
        db.session.commit()

       # else (user is in database)
    #     Need to check password

    return render_template("register_form.html")

@app.route('/users')
def user_list():
    """ Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
