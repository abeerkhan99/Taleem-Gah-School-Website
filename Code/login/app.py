from flask import Flask, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
import psycopg2

# app instance
app = Flask(__name__)
# for sessions
app.secret_key = 'BAD_SECRET_KEY'

# ENV = 'dev'
# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/taleem-gah' #change this to your database settings

# else:
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = ''

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disables warnings

# # create database object 
# db = SQLAlchemy(app)
# session = Session(engine)

def get_db_connection():
    conn = psycopg2.connect(
            host="localhost",
            database="taleem-gah",
            user= 'postgres',
            password= '12345')

    return conn

# Open a cursor to perform database operations
conn = get_db_connection()
cur = conn.cursor()

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

@app.route('/submit', methods = ['GET', 'POST'])
def submit():
    if request.method == 'POST':
        user_name = request.form['uname']
        password = request.form['pass']
        print("PASSWORD IS:", password)
        # print(email, password)
        if user_name == '' and password == '':
            return render_template('login.html', message = "Please enter required fields")
        elif user_name == '' and password != '':
            return render_template('login.html', message = "Please enter your username")
        elif user_name != '' and password == '':
            return render_template('login.html', message = "Please enter your password")
        
        else:
            # fields entered
            # check username exists
            cur.execute('SELECT Username from faculty where Username = %s', (user_name,))
            user_object = cur.fetchall() 

            print(user_object[0][0])

            if user_object == user_name:
                return render_template('login.html', message = "This username does not exist")
            else:
                #check password 
                cur.execute('SELECT Pass from faculty where Username = %s', (user_name,))
                user_password = cur.fetchall()

                print(user_password[0][0])

                if user_password[0][0] == password:

                    print("TRUE")
                    cur.execute('SELECT FirstName, LastName from faculty where Username = %s AND Pass = %s', (user_name, password))
                    faculty_name = cur.fetchall()

                    faculty_name_string = faculty_name[0][0] + ' ' + faculty_name[0][1]
                    session['user_info'] = faculty_name_string

                    # check if user is teacher or admin
                    cur.execute('SELECT faculty_type from faculty where Username = %s AND Pass = %s', (user_name, password))
                    faculty_type = cur.fetchall()

                    print('FACULTY TYPE IS:', faculty_type[0][0])

                    if faculty_type[0][0] == 'Admin': 
                        return redirect(url_for('admin_homepage'))
                    elif faculty_type[0][0] == 'Teacher':
                        return redirect(url_for('teacher_homepage'))
                else:
                    print("FALSE")
                    return render_template('login.html', message = "Incorrect Password!")
    cur.close()
    conn.close()
    return 


@app.route('/admin-homepage')
def admin_homepage():
    return render_template('admin-homepage.html')
    # return 'Hello World!'

@app.route('/teacher-homepage')
def teacher_homepage():
    return render_template('teacher-homepage.html')
    # return 'Hello World!'

if __name__ == '__main__':
    app.run()
