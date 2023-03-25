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


@app.route('/admin-homepage')
def admin_homepage():
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0 and session.get('user_info_type') == 'Admin':
        return render_template('admin-homepage.html')
    else:
        return redirect(url_for('login'))

@app.route('/teacher-homepage')
def teacher_homepage():
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0 and session.get('user_info_type') == 'Teacher':
        return render_template('teacher-homepage.html')
    else:
        return render_template('login')
