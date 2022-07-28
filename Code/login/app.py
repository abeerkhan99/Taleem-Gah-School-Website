from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

# app instance
app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/taleem-gah' #change this to your database settings

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disables warnings

# create database object 
db = SQLAlchemy(app)

# create model
class user(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)

    # constructor
    def __init__(self, username, password):
        self.username = username
        self.password = password

# routing
@app.route('/')
def home():
    return render_template('welcome.html')
    # return 'Hello World!'

@app.route('/login')
def login():
    return render_template('login.html')
    # return 'Hello World!'

@app.route('/logout')
def logout():
    return render_template('login.html')
    # return 'Hello World!'

@app.route('/registration')
def register():
    return render_template('register.html')
    # return 'Hello World!'

@app.route('/verify-details')
def verify():
    return render_template('verify.html')
    # return 'Hello World!'

@app.route('/reset')
def reset_pass():
    return render_template('reset-pass.html')
    # return 'Hello World!'

@app.route('/submit', methods = ['POST'])
def submit():
    if request.method == 'POST':
        email = request.form['uname']
        password = request.form['pass']
        # print(email, password)

        # check username exists
        

        if email == '' and password == '':
            return render_template('login.html', message = "Please enter required fields")
        elif email == '' and password != '':
            return render_template('login.html', message = "Please enter your email address")
        elif email != '' and password == '':
            return render_template('login.html', message = "Please enter your password")
        
        else:
            return render_template('homepage.html')


if __name__ == '__main__':
    app.run()
