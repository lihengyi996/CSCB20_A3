from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text # textual queries

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 15)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Person(db.Model):
    __tablename__ = "LoginInfo"
    id = db.Column(db.Integer, primary_key = True)
    utorid = db.Column(db.String(20), unique=True, nullable = False)
    password_hashed = db.Column(db.String(20), nullable = False)
    identity = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"Person('{self.utorid}', '{self.identity}')"

@app.route('/')
@app.route('/home')
def home():
    pagename = 'home'
    return render_template('home.html', pagename = pagename)

@app.route('/staff')
def staff():
    pagename = 'staff'
    return render_template('staff.html', pagename = pagename)

@app.route('/news')
def news():
    pagename = 'news'
    return render_template('news.html', pagename = pagename)

@app.route('/calendar')
def calendar():
    pagename = 'calendar'
    return render_template('calendar.html', pagename = pagename)

@app.route('/assignment_lab')
def assignment_lab():
    pagename = 'assignment_lab'
    return render_template('assignment_lab.html', pagename = pagename)

@app.route('/lecture')
def lecture():
    pagename = 'lecture'
    return render_template('lecture.html', pagename = pagename)

@app.route('/AnonFeedback')
def AnonFeedback():
    pagename = 'AnonFeedback'
    return render_template('AnonFeedback.html', pagename = pagename)

@app.route('/resources')
def resources():
    pagename = 'resources'
    return render_template('resources.html', pagename = pagename)

if __name__ == '__main__':
    app.run(debug=True)
