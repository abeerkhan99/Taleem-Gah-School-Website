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

@app.route('/verify-details')
def verify():
    return render_template('verify_homepage.html')


@app.route('/verification', methods = ['GET', 'POST'])
def verify_submit():
    if request.method == 'POST':
        user_name = request.form['u_name']
        user_number = request.form['u_number']

        cur.execute('SELECT Username from faculty where Username = %s and PhoneNo = %s', (user_name, user_number,))
        user_name_object = cur.fetchall()

        cur.execute('SELECT PhoneNo from faculty where Username = %s and PhoneNo = %s', (user_name, user_number,))
        user_number_object = cur.fetchall()

        # check if username and number exists 
        if len(user_name_object) != 0 and len(user_number_object) != 0:

            user_name_item = user_name_object.pop()
            user_name_string = ''.join(user_name_item)

            user_number_item = user_number_object.pop()
            user_number_string = ''.join(user_number_item)

            session['reset_u_name'] = user_name_string
            session['reset_u_number'] = user_number_string

            return redirect(url_for('reset_pass'))
        else:
            return render_template('verify_homepage.html', message = "This account does not exist.")
    return


@app.route('/reset')
def reset_pass():
    return render_template('reset-pass.html')
    # return 'Hello World!'


@app.route('/reset-submit', methods = ['GET', 'POST'])
def reset_pass_submit():
    if len(session.get('reset_u_name')) != 0 and len(session.get('reset_u_number')) != 0:

        if request.method == 'POST':
            user_new_pass = request.form['new_pass']

            # alter table details
            cur.execute("UPDATE faculty SET Pass = %s WHERE Username = %s AND PhoneNo = %s", (user_new_pass, session.get('reset_u_name'), session.get('reset_u_number'),))
            
            # save changes to database
            conn.commit()

            # clear session data
            session.pop('reset_u_name', default=None)
            session.pop('reset_u_number', default=None)

            return render_template('reset-pass.html', message = "Password changed. You may log in now with the new password.")
    else:
        return redirect(url_for('verify'))

