# Server

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.sqlite3'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column('messageID', db.Integer, primary_key=True)
    mess = db.Column(db.Text(500))
    date = db.Column(db.String(10))

    # Constructor
    def __init__(self, mess, date):
        self.mess = mess
        self.date = date

    # Overwrite print
    def __repr__(self):
        return '%s -> %s' % self.date, self.mess

@app.route('/')
def index():
    message = Message('HELLO WORLD', getToday())
    db.session().add(message)
    db.session().commit()
    return render_template('index.html')


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
    app.run()
