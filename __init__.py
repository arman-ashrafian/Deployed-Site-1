# Server

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import os
import owm
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'
db = SQLAlchemy(app)

no_post = False         # true if submitted blog post is empty
login_failed = False    # true if login failed

# Admin login
ADMIN_USER = "ashy63"
ADMIN_PASS = "password"

# Session secret key
app.secret_key = 'SECRETKEY'


# Database Table: Blog
# blog_id (primary key)           post                            date
# ------------------------------  ------------------------------  ----------


class Blog(db.Model):
    id = db.Column('blog_id', db.Integer, primary_key=True)
    post = db.Column(db.String(1000))
    date = db.Column(db.String(10))

    # Constructor
    def __init__(self, post, date):
        self.post = post
        self.date = date

    # Redefining print function
    def __repr__(self):
        return '%r' % self.post

# Home Page


@app.route("/")
def index():
    # Link to get weather icon
    icon_link = 'http://openweathermap.org/img/w/%s.png' % owm.getIcon()

    # Check if logged in
    loggedIn = checkLogin()

    return render_template("index.html", weather_icon=icon_link,
                           current_temp=owm.getTemp(),
                           max_temp=owm.getTempMax(),
                           min_temp=owm.getTempMin(),
                           humidity=owm.getHumidity(),
                           logged_in=loggedIn)

# Login Page


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # If empty form
        if not request.form['user'] or not request.form['pass']:
            return render_template("login.html", no_data=True,
                                   login_failed=False)
        else:
            # Correct login
            if request.form['user'] == ADMIN_USER and request.form['pass'] == ADMIN_PASS:
                # Set session username
                session['username'] = request.form['user']

                return redirect(url_for('index'))

            # Incorrect login
            else:
                return render_template("login.html", no_data=False,
                                       login_failed=True)

    return render_template("login.html", no_data=False,
                           login_failed=False)

# Logout Page


@app.route("/logout", methods=["GET"])
def logout():
    if request.method == "GET":
        if 'username' in session:
            # remove user from session
            session.pop('username', None)

    # Redirect to home page
    return redirect(url_for('index'))

# Blog Page


@app.route("/blog")
def blog():
    global no_post

    loggedIn = checkLogin()

    return render_template("blog.html", blogs=Blog.query.all(),
                           empty_post=no_post,
                           logged_in=loggedIn)

# New blog post processing


@app.route("/newpost", methods=["GET", "POST"])
def new_post():
    global no_post

    if request.method == "POST":
        # If post is empty
        if not request.form['newpost']:
            no_post = True
        else:
            no_post = False

            today = getToday()  # get date
            post = Blog(request.form['newpost'], today)  # create DB object

            postID = post.id

            db.session.add(post)
            db.session.commit()

    return redirect(url_for('blog'))

# Delete post processing


@app.route("/delete_post/<int:ID>", methods=["POST"])
def delete_post(ID):
    # post to be deleted
    post = Blog.query.filter_by(id=ID).first()

    # delete the post
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("blog"))

# Projects Page


@app.route("/projects")
def projects():
    return render_template("projects.html")

# Check Login
# returns true if user is logged in
def checkLogin():
    loggedIn = False
    if 'username' in session:
        if session['username'] == "ashy63":
            loggedIn = True
    return loggedIn

# Get Today
# returns formatted date as a string
def getToday():
    today = str(datetime.date.today())
    year = today[:4]
    month = today[5:7]
    day = today[8:]

    return '%s-%s-%s' % (month, day, year)

if __name__ == "__main__":

    # declaring host and port
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 8080)),
            debug=True)
