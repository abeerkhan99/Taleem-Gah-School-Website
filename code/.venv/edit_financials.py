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


@app.route('/view-financial-record')
def edit_view_financials():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin'):
        
        years = financials.main("info", [datetime.datetime.today()])
        return render_template('select_edit_financial_record.html', year = years)

    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/edit-financials', methods = ['GET', 'POST'])
def edit_financials():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin'):

        if request.method == 'POST':
            start_month = int(request.form.get('start_financial_month_edit'))
            start_year = int(request.form.get('start_financial_year_edit'))
  
            # retrieve info from csv file using dates given
            balance_info = financials.main('total', [datetime.datetime(start_year, start_month, 12)], [datetime.datetime(start_year, start_month, 12)])

            if balance_info == [0]:
                return render_template('select_edit_financial_record.html', message = "No records present for this month")
            else:
                return render_template('edit_financial_record.html', balance = balance_info, start_month = start_month, start_year = start_year, len_balance = len(balance_info)-1)
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/edit-financials-submit', methods = ['GET', 'POST'])
def edit_financials_submit():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin'):
        
        # form submit returns a variable
        # according to variable content can be added or deleted entirely
        if request.method == "POST":
            month = int(request.form['e_month'])
            year = int(request.form['e_year'])

            balance_info = financials.main('total', [datetime.datetime(year, month, 12)], [datetime.datetime(year, month, 12)])
            
            print(balance_info)

            donation_info = []
            expense_info = []

            for x in range(len(balance_info) - 1):
                if balance_info[x][2][1] > 0:
                    try:
                        # print(balance_info[x][2])
                        dname = request.form["d" + str(x)]
                        damount = int(request.form["da" + str(x)])
                    
                        donation_info.append([dname, damount])
                    except:
                        pass

                elif balance_info[x][2][1] < 0:
                    try:
                        ename = request.form["e" + str(x)]
                        eamount = -(int(request.form["ea" + str(x)]))

                        print(ename, eamount)

                        expense_info.append([ename, eamount])
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

        # delete balance already existing in file of the chosen month
        financials.main('delete', [datetime.datetime(year, month, 12)])

        # add new balance in file
        print("DONATION: ", donation_info)
        print("EXPENSE: ", expense_info)

        # if donation and expense is empty, don't add anything in file
        if len(donation_info) == 0 and len(expense_info) == 0:
            pass
        else:
            # add in file
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

        balance_info = financials.main('total', [datetime.datetime(year, month, 12)], [datetime.datetime(year, month, 12)])

        return render_template('edit_financial_record.html', message = "Updated!", balance = balance_info, start_month = month, start_year = year, len_balance = len(balance_info)-1)

    else:
        return redirect(url_for('login', message = "Please login."))
