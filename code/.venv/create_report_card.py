from ast import excepthandler
from hmac import new
from pickletools import read_uint1
from flask import Flask, render_template, url_for, request, session, redirect, jsonify
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

@app.route('/choose-a-class', methods = ['GET', 'POST'])
def class_picker():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        
        # pick class from list of classes
        cur.execute('SELECT class_name from classes')
        list_of_classes = cur.fetchall()

        return render_template('choose-a-class.html', classes = list_of_classes )
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/choose-a-semester', methods = ['GET', 'POST'])
def semester_picker():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
    
        class_name = request.form['c_name']
        session['class_name'] = class_name

        # pick semester 
        cur.execute('SELECT class_Semester from class_has_semester WHERE class_classesName = %s', (class_name,))
        list_of_semesters = cur.fetchall()
        
        return render_template('choose-a-semester.html', semester = list_of_semesters)
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/create-a-report-card', methods = ['GET', 'POST'])
def create_a_report_card():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
    
        semester_name = request.form['s_name']
        session['semester_name'] = semester_name

        # find number of subjects 
        cur.execute('SELECT class_subjectName from class_has_subject WHERE class_classesName = %s', (session.get('class_name'),))
        list_of_subjects = cur.fetchall()

        session['total_subjects'] = list_of_subjects
        
        return render_template('create-a-report-card.html', semester = semester_name, classes = session.get('class_name'), subjects = list_of_subjects, length_subject = len(list_of_subjects))
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/create-a-report-card-submit', methods = ['GET', 'POST'])
def create_a_report_card_submit():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
    
        if request.method == 'POST':
            # get info from form
            studentfirst = request.form['student_firstname']
            studentlast = request.form['student_lastname']
            classname = request.form['classname']
            semestername = request.form['semestername'][-1]
            total_working = request.form['totalworkingdays']
            s_attendance = request.form['studentattendance']

            session['first_name'] = studentfirst
            session['last_name'] = studentlast

            total_marks = []
            marks = []
            for x in range(len(session.get('total_subjects')) * 4):
                if x % 4 == 0:
                    if len(marks) != 0:
                        total_marks.append(marks)
                    marks = []
                    marks.append(request.form[str(x)])
                else:
                    marks.append(request.form[str(x)])
            total_marks.append(marks)
            print(total_marks)

            # add form info into marks table
            # subject, obtained marks, passing marks, total marks
            # overwrite data if exists
            for x in total_marks:
                # check if information is already in the database
                cur.execute('SELECT count(*) from marks WHERE FirstName = %s and LastName = %s and class_Name = %s and subject_Name = %s and semester_Name = %s and Marks = %s and Passing_Marks = %s and Total_Marks = %s',
                            (studentfirst, studentlast, classname, x[0], semestername, x[1], x[2], x[3],))
                mark_exist = cur.fetchall()

                if mark_exist[0][0] == 0:
                    # add info in database
                    cur.execute('INSERT INTO marks (FirstName, LastName, class_Name, semester_Name, subject_Name, Total_Marks, Passing_Marks, Marks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                                (studentfirst, studentlast, classname, semestername, x[0], x[3], x[2], x[1],))
                    conn.commit()

                elif mark_exist[0][0] != 0:
                    # show dialog box asking user if they want to update the report card or not
                    # have a view report card option
                    # update info in database
                    cur.execute('UPDATE marks SET Total_Marks = %s, Passing_Marks = %s, Marks = %s WHERE FirstName = %s and LastName = %s and class_Name = %s and semester_Name = %s and subject_Name = %s', 
                            (x[3], x[2], x[1], studentfirst, studentlast, classname, semestername, x[0],))
                    conn.commit()


            # add attendance
            # check if information is already in the database
            cur.execute('SELECT count(*) from student_has_attendance WHERE FirstName = %s and LastName = %s and class_classesName = %s and semester_semesterName = %s', (studentfirst, studentlast, classname, semestername))
            attendance_data_object = cur.fetchall()

            #if information exists, then overwrite information in the database
            if attendance_data_object[0][0] == 0:
                cur.execute('INSERT into student_has_attendance(FirstName, LastName, class_classesName, semester_semesterName, totalWorkingDays, student_attendance) VALUES (%s,%s,%s,%s,%s,%s)', 
                            (studentfirst, studentlast, classname, semestername, total_working, s_attendance,))
                conn.commit()
            
            # overwrite
            elif attendance_data_object[0][0] != 0:
                cur.execute('UPDATE student_has_attendance SET totalWorkingDays = %s, student_attendance = %s WHERE FirstName = %s and LastName = %s and class_classesName = %s and semester_semesterName = %s',
                            (total_working, s_attendance, studentfirst, studentlast, classname, semestername,))
                conn.commit()
            
            message = "Report card generated! Would you like to generate another one?"
            return jsonify(message=message)
            
            # return render_template('create-a-report-card.html', message = "Report generated! Would you like to generate another one?", semester = session.get('semestername'), classes = session.get('class_name'), subjects = session.get('total_subjects'), length_subject = len(session.get('total_subjects')))

        else:
            message = "Not able to add report card in the system."
            return jsonify(message=message)
            # return render_template('create-a-report-card.html', message = "Not able to add report card in the system.", semester = session.get('semestername'), classes = session.get('class_name'), subjects = session.get('total_subjects'), length_subject = len(session.get('total_subjects')))
    else:
        return redirect(url_for('login', message = "Please login."))
