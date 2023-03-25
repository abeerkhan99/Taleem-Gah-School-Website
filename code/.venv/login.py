from ast import excepthandler
from hmac import new
from pickletools import read_uint1
from flask import Flask, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL, create_engine, delete
from sqlalchemy.orm import Session
import os
import psycopg2
from fpdf import FPDF
import pandas as pd
import financials
import datetime
from pdf import my_pdf
from app import app
from app import conn, cur


@app.route('/login')
def login():
    return render_template('welcome.html')
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
            user_object_string = None

            #make user_object into string
            if user_object != []:
                user_object_item = user_object.pop()
                user_object_string = ''.join(user_object_item)

            # if username exists, then check password and username combo 
            if user_object_string != user_name:
                return render_template('welcome.html', message = "This username does not exist")

            else:
                #check password 
                cur.execute('SELECT Pass from faculty where Username = %s', (user_name,))
                user_password = cur.fetchall()
                user_password_string = None

                if user_password != []:
                    user_password_item = user_password.pop()
                    user_password_string = ''.join(user_password_item)
                
                if user_password_string != password:
                    print("FALSE")
                    return render_template('welcome.html', message = "Incorrect Password!")
                else:
                    print("TRUE")

                    cur.execute('SELECT FirstName, LastName from faculty where Username = %s AND Pass = %s', (user_name, password))
                    faculty_name = cur.fetchall()

                    faculty_name_string = faculty_name[0][0] + ' ' + faculty_name[0][1]

                    # check if user is teacher or admin
                    cur.execute('SELECT faculty_type from faculty where Username = %s AND Pass = %s', (user_name, password))
                    faculty_type = cur.fetchall()

                    session['user_info_name'] = faculty_name_string
                    session['user_info_username'] = user_object_string
                    session['user_info_type'] = faculty_type[0][0]

                    if faculty_type[0][0] == 'Admin': 
                        return redirect(url_for('admin_homepage'))
                    elif faculty_type[0][0] == 'Teacher':
                        return redirect(url_for('teacher_homepage'))
    return 

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
    # return 'Hello World!'
