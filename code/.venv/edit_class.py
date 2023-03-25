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

@app.route('/choose-a-class-to-edit')
def pick_class_edit():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        
        # pick class from list of classes
        cur.execute('SELECT class_name from classes')
        list_of_classes = cur.fetchall()

        return render_template('pick-a-class-to-edit.html', classes = list_of_classes )
    else:
        return redirect(url_for('login', message = "Please login."))

@app.route('/edit-class')
def edit_class():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        
        if request.method == 'POST':
            class_name = request.form['c']

            # fetch subjects connected to the class
            cur.execute('SELECT class_subjectName from class_has_subject WHERE class_classesName = %s', (class_name,))
            class_subjects = cur.fetchall()

            # fetch all subjects from the database
            cur.execute('SELECT SubjectName from subject')
            all_subjects = cur.fetchall()

        return render_template('edit-a-class.html', subjects = class_subjects, classname = class_name, all_subjects = all_subjects)
    else:
        return redirect(url_for('login', message = "Please login."))
