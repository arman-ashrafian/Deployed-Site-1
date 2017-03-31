
# Server

from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Example(db.Model):
    __tablename__ = "Example"
    id = db.Column('id', db.Integer, primary_key=True)
    data = db.Column('data', db.Unicode)

    # Constructor
    def __init__(self, text):
        self.data = text


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new', methods=["POST"])
def new():
    if(request.method == "POST"):
        userText = request.form['text']
        if(userText != None):
            dbEntery = Example(userText)
            db.session.add(dbEntery)
            db.session.commit()

    return redirect(url_for('index'))

# Get Today
# returns formatted date as a string
def getToday():
    today = str(datetime.date.today())
    year = today[:4]
    month = today[5:7]
    day = today[8:]

    return '%s-%s-%s' % (month, day, year)

if __name__ == "__main__":
    # start server
    app.run(debug=True)
