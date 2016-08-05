"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, url_for, render_template, redirect, request, flash, session)
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
   
    if not user:
        user = User(email=emailaddress,
                    password=password)
        
        db.session.add(user) 
        db.session.commit()
        flash("Account created.")
        return redirect('/')

    if user.password != password:
        flash("Incorrect password.")
        return redirect(url_for("register_form"))

    flash("Logged in.")
    return redirect('/')

@app.route('/users')
def user_list():
    """ Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/user_details/<user_id>')
def user_details(user_id):
    """ show users rated movies """
    
    user = User.query.get(user_id)
    ratings = Rating.query.filter_by(user_id=user.user_id).all()
    
    return render_template("user_details.html", user=user, ratings=ratings)

#From rating grab every movie title and rating for that user



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
