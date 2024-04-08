from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text # textual queries

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cscb20db.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 15)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

session_id = 1

class Person(db.Model):
    __tablename__ = "LoginInfo"
    id = db.Column(db.Integer, primary_key = True)
    utorid = db.Column(db.String(20), unique=True, nullable = False)
    password_hashed = db.Column(db.String(20), nullable = False)
    identity = db.Column(db.String(20), nullable = False, default='student')

    def __repr__(self):
        return f"Person('{self.utorid}', '{self.identity}')"

class Grade(db.Model):
    __tablename__ = "studentGrade"
    id = db.Column(db.Integer, primary_key = True)
    midterm = db.Column(db.Float)
    final = db.Column(db.Float)
    assignment1 = db.Column(db.Float)
    assignment2 = db.Column(db.Float)
    assignment3 = db.Column(db.Float)
    lab1 = db.Column(db.Float)
    lab2 = db.Column(db.Float)
    lab3 = db.Column(db.Float)

    def __repr__(self):
        return f"Grade('{self.final}', '{self.midterm}')"
    
class anonFeedback(db.Model):
    __tablename__ = "anonFeedback"
    feedbackID = db.Column(db.Integer, primary_key=True)
    content_teaching_good = db.Column(db.Text)
    content_teaching_bad = db.Column(db.Text)
    content_assignment_good = db.Column(db.Text)
    content_assignment_bad = db.Column(db.Text)

@app.route('/test_db')

def test_db():
    try:
        db.session.query(Person).first()
        return "Connected to the database successfully!"
    except Exception as e:
        return "An error occurred when connecting to the database: " + str(e)

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

@app.route('/AnonFeedback', methods = ['GET', 'POST'])
def AnonFeedback():
    if request.method == 'GET':
        return render_template('AnonFeedback.html')
    else:
        feedback = anonFeedback(
        content_teaching_good=request.form['content_teaching_good'],
        content_teaching_bad=request.form['content_teaching_bad'],
        content_assignment_good=request.form['content_assignment_good'],
        content_assignment_bad=request.form['content_assignment_bad']
        )

    db.session.add(feedback)
    db.session.commit()
    return render_template('AnonFeedback.html')

@app.route('/resources')
def resources():
    pagename = 'resources'
    return render_template('resources.html', pagename = pagename)

@app.route('/marks', methods = ['GET', 'POST'])
def marks():
    if request.method == 'GET':
        query_marks_result = query_marks(2)
        return render_template('marks.html', query_marks_result = query_marks_result)
    
@app.route('/add_dummy_grade', methods=['GET'])
def add_grade():
    new_grade = Grade(id=1, midterm=85.0, final=90.0, assignment1=80.0, assignment2=82.0, assignment3=88.0, lab1=95.0, lab2=92.0, lab3=91.0)
    db.session.add(new_grade)
    db.session.commit()
    return "Grade added successfully", 200
    
def query_marks(id):
    marks = Grade.query.filter_by(id=session_id)
    return marks

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            flash('already logged in!!')
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        utorid = request.form['UTorID']
        password = request.form['Password']
        person = Person.query.filter_by(utorid = utorid).first()
        if not person or not bcrypt.check_password_hash(person.password_hashed, password):
            flash('Please check your login details and try again', 'error')
            return render_template('login.html')
        else:
            session['name'] = utorid
            session.permanent = True
            return redirect(url_for('home'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        utorid = request.form['UTorID']
        identity = request.form['Identity']
        hashed_password = bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        reg_details =(
            utorid,
            identity,
            hashed_password
        )
        add_users(reg_details)
        flash('Registration Successful! Please login now:')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('name', default = None)
    return redirect(url_for('home'))

def add_users(reg_details):
    person = Person(utorid = reg_details[0], identity = reg_details[1], password_hashed = reg_details[2])
    db.session.add(person)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
