from ast import excepthandler
from hmac import new
from math import e
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


@app.route('/financial-records-homepage')
def financial_records_homepage():
    return render_template('view_financial_records_admin_homepage.html')
    # return 'Hello World!'

@app.route('/create-financials')
def create_financials():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin'):
        
        return render_template('create_financial_record.html')

    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/create-financials-submit', methods = ['GET', 'POST'])
def create_financials_submit():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin'):

        if request.method == 'POST':
            month = int(request.form.get('add_financial_month'))
            year = int(request.form.get('add_financial_year'))

            donation_info = []
            expense_info = []

            try:
                donation_name1 = request.form['name_donation']
                donation_amount1 = int(request.form['donation_amount'])

                donation_info.append([donation_name1, donation_amount1])
            except:
                pass

            try:
                expense_name1 = request.form['name_expense']
                expense_amount1 = -(int(request.form['expense_amount']))

                expense_info.append([expense_name1, expense_amount1])
            except:
                pass

            d_name = 1
            d_amount = 3
            
            e_name = 2
            e_amount = 4

            while d_name >= 1 and d_amount >= 3:
                try:
                    donation_name2 = request.form[str(d_name)]
                    donation_amount2 = int(request.form[str(d_amount)])

                    donation_info.append([donation_name2, donation_amount2])

                    d_name = d_name + 2
                    d_amount = d_amount + 2
                except:
                    break
            
            while e_name >= 2 and e_amount >= 4:
                try:
                    expense_name2 = request.form[str(e_name)]
                    expense_amount2 = -(int(request.form[str(e_amount)]))

                    expense_info.append([expense_name2, expense_amount2])

                    e_name = e_name + 2
                    e_amount = e_amount + 2

                except:
                    break

            if len(donation_info) == 0 and len(expense_info) == 0:
                return render_template('create_financial_record.html', message = "You have not added any records!")
            else:
                if len(donation_info) == 0:
                    pass
                else:
                    for d in donation_info:
                        financials.main('add', [datetime.datetime(year, month, 12), d[0], d[1]])
                
                if len(expense_info) == 0:
                    pass
                else:
                    for e in expense_info:
                        financials.main('add', [datetime.datetime(year, month, 12), e[0], e[1]])

                return render_template('create_financial_record.html', message = "Financials added!")

    else:
        return redirect(url_for('login', message = "Please login."))
