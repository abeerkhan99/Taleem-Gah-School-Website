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

def what_month(month):
    if month == 1:
        return "January"
    elif month == 2:
        return "February"
    elif month == 3:
        return "March"
    elif month == 4:
        return "April"
    elif month == 5:
        return "May"
    elif month == 6:
        return "June"
    elif month == 7:
        return "July"
    elif month == 8:
        return "August"
    elif month == 9:
        return "September"
    elif month == 10:
        return "October"
    elif month == 11:
        return "November"
    elif month == 12:
        return "December"

@app.route('/select-date')
def financial_date_select():

    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin'):
        
        years = financials.main("info", [datetime.datetime.today()])

        print(years)
        return render_template('financial-sheet.html', year = years)

    else:
        return redirect(url_for('login', message = "Please login."))
    # return 'Hello World!'

@app.route('/financial_date_submit', methods = ['GET', 'POST'])
def financial_date_submit():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin'):
        
        if request.method == 'POST':
            start_month = int(request.form.get('start_financial_month'))
            start_year = int(request.form.get('start_financial_year'))

            end_month = int(request.form.get('end_financial_month'))
            end_year = int(request.form.get('end_financial_year'))

            donationcount = 0
            expensecount = 0
  
            # retrieve info from csv file using dates given
            balance_info = financials.main('total', [datetime.datetime(start_year, start_month, 12)], [datetime.datetime(end_year, end_month, 12)])

            for x in range(len(balance_info)-1):
                m = what_month(balance_info[x][0])
                balance_info[x][0] = m
                if balance_info[x][2][1] > 0:
                    donationcount += 1
                
                elif balance_info[x][2][1] < 0:
                    expensecount += 1

            print(balance_info)

            if balance_info == [0]:
                years = financials.main("info", [datetime.datetime.today()])
                return render_template('financial-sheet.html', message = "No records present for these months", year = years)
            else:
                return render_template('view-financial-records.html', donationcount = donationcount, expensecount = expensecount, balance = balance_info, start_month = what_month(start_month), start_year = start_year, end_month = what_month(end_month), end_year = end_year, len_balance = len(balance_info)-1)
    else:
        return redirect(url_for('login', message = "Please login."))


    
