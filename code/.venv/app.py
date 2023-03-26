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

# app instance
app = Flask(__name__, template_folder='templates')
# for sessions
app.secret_key = 'BAD_SECRET_KEY'

def get_db_connection():
    conn = psycopg2.connect(
            host="dpg-cgg47nu4daddcg25rtj0-a",
            database="taleemgah",
            user= 'taleemgah_user',
            password= 'S0qoU8kEq04dYNe1q43RQJgmbyZ77BC4')

    return conn

# Open a cursor to perform database operations
conn = get_db_connection()
cur = conn.cursor()

# routing
@app.route('/')
def home():
    return render_template('welcome.html')
    # return 'Hello World!'

import login
import verification

import homepage
import edit_class
import create_report_card
import view_report_card
import view_financials
import create_financials
import edit_financials

if __name__ == '__main__':
    app.run()