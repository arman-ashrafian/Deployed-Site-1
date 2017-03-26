
# Server

from flask import Flask, render_template
import datetime

app = Flask(__name__)
@app.route('/')
def index():
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
