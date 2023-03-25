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

# make function to get all report cards stored in db for that class and semester
@app.route('/choose-class', methods = ['GET', 'POST'])
def choose_class():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        
        # pick class from list of classes
        cur.execute('SELECT class_name from classes')
        list_of_classes = cur.fetchall()

        return render_template('choose-class.html', classes = list_of_classes )
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/choose-semester', methods = ['GET', 'POST'])
def choose_semester():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
    
        class_name = request.form['c_name']
        session['class_name'] = class_name

        # pick semester 
        cur.execute('SELECT class_Semester from class_has_semester WHERE class_classesName = %s', (class_name,))
        list_of_semesters = cur.fetchall()

        return render_template('choose-semester.html', semester = list_of_semesters)
    else:
        return redirect(url_for('login', message = "Please login."))
    
@app.route('/view-report-cards', methods = ['GET', 'POST'])
def view_report_cards():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
    
        semester_name = request.form['s_name']
        session['semester_name'] = semester_name

        cur.execute('SELECT distinct FirstName, LastName from marks WHERE semester_Name = %s and class_Name = %s', (semester_name, session.get('class_name')))
        student_records_object = cur.fetchall()

        if len(student_records_object) == 0:
            # No records found
            return render_template('choose-class.html', message = "No records found for this class and semester.")
        else:
            return render_template('view-report-cards.html', len = len(student_records_object), student_records_object = student_records_object)
    else:
        return redirect(url_for('login', message = "Please login."))
    
@app.route('/view-a-report-card', methods = ['GET', 'POST'])
def view_a_report_card():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        if request.method == 'POST':

            first_name = request.form['0']
            last_name = request.form['1']

            session['first_name'] = first_name
            session['last_name'] = last_name

            print(first_name)
            print(last_name)

            print(session.get('class_name'), session.get('semester_name'))

            # fetch the subject marks
            cur.execute('SELECT subject_Name, Marks, Passing_Marks, Total_Marks from marks WHERE class_Name = %s and semester_Name = %s and FirstName = %s and LastName = %s', (session.get('class_name'), session.get('semester_name'), first_name, last_name))
            marks = cur.fetchall()

            # fetch student attendance
            cur.execute('SELECT totalWorkingDays, student_attendance from student_has_attendance WHERE FirstName = %s and LastName = %s and class_classesName = %s and semester_semesterName = %s', (first_name, last_name, session.get('class_name'), session.get('semester_name')))
            attendance = cur.fetchall()
            print(attendance)

            return render_template('view-a-report-card.html', length = len(marks), firstname = first_name, lastname = last_name, classname = session.get('class_name'), semestername = session.get('semester_name'), marks = marks, attendance = attendance)
    else:
        return redirect(url_for('login', message = "Please login."))
    

@app.route('/edit-a-report-card', methods = ['GET', 'POST'])
def edit_a_report_card():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        if request.method == 'POST':

            first_name = request.form['0']
            last_name = request.form['1']

            # fetch the subject marks
            cur.execute('SELECT subject_Name, Marks, Passing_Marks, Total_Marks from marks WHERE class_Name = %s and semester_Name = %s and FirstName = %s and LastName = %s', (session.get('class_name'), session.get('semester_name'), first_name, last_name))
            marks = cur.fetchall()

            # fetch student attendance
            cur.execute('SELECT totalWorkingDays, student_attendance from student_has_attendance WHERE FirstName = %s and LastName = %s and class_classesName = %s and semester_semesterName = %s', (first_name, last_name, session.get('class_name'), session.get('semester_name')))
            attendance = cur.fetchall()

            return render_template('view-a-report-card.html', length = len(marks), id = session.get('student_id'), firstname = session.get('student_f_name') , lastname = session.get('student_l_name') , gender = session.get('student_g'), classname = class_name, semestername = semester_name, marks = marks, attendance = attendance)
    else:
        return redirect(url_for('login', message = "Please login."))
    
@app.route('/delete-a-report-card', methods = ['GET', 'POST'])
def delete_a_report_card():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        if request.method == 'POST':

            first_name = request.form['0']
            last_name = request.form['1']

            # delete the subject marks
            cur.execute("DELETE FROM marks WHERE FirstName = %s and LastName = %s and class_Name = %s and semester_Name = %s", first_name, last_name, session.get('semester_name'), session.get('class_name'))
            conn.commit()

            # delete the attendance record
            cur.execute("DELETE FROM student_has_attendance WHERE FirstName = %s and LastName = %s and class_classesName = %s and semester_semesterName = %s", first_name, last_name, session.get('class_name'), session.get('semester_name'))
            conn.commit()

            # fetch all results for the semester and class 
            cur.execute('SELECT distinct FirstName, LastName from marks WHERE semester_Name = %s and class_Name = %s', (session.get('semester_name'), session.get('class_name')))
            student_records_object = cur.fetchall()

            if len(student_records_object) == 0:
                # No records found
                return render_template('choose-class.html', message = "No records found for this class and semester.")
            else:
                return render_template('view-report-cards.html', len = len(student_records_object), student_records_object = student_records_object) 
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/generate-pdf')
def generate_pdf():

    # fetch the subject marks
    cur.execute('SELECT subject_Name, Marks, Passing_Marks, Total_Marks from marks WHERE class_Name = %s and FirstName = %s and LastName = %s and semester_Name = %s', (session.get('class_name'), session.get('first_name'), session.get('last_name'), session.get('semester_name'),))
    marks = cur.fetchall()

    print(session.get('class_name'), session.get('first_name'), session.get('last_name'), session.get('semester_name'))

    # fetch student attendance
    cur.execute('SELECT totalWorkingDays, student_attendance from student_has_attendance WHERE FirstName = %s and LastName = %s and class_classesName = %s and semester_semesterName = %s', (session.get('first_name'), session.get('last_name'), session.get('class_name'), session.get('semester_name'),))
    attendance = cur.fetchall()

    subjects = []
    passingMarks = []
    totalMarks = []
    marksObtained = []

    for s in marks:
        subjects.append(s[0])
        marksObtained.append(int(s[1]))
        passingMarks.append(int(s[2]))
        totalMarks.append(int(s[3]))

    overall_percentage = round((sum(marksObtained)/sum(totalMarks)) * 100, 1)

    marksObtained.append(sum(marksObtained))
    passingMarks.append(str(overall_percentage) + '%')
    totalMarks.append(sum(totalMarks))
    subjects.append("Total Marks")

    full_name = session.get('first_name') + " " + session.get('last_name')
    student_attendance = attendance[0][1]
    working_days = attendance[0][0]
    path_name = session.get('first_name') + '-' + session.get('last_name') + '-' + session.get('class_name') + '-' + 'Semester ' + session.get('semester_name') + '.pdf'

    my_pdf(subjects, marksObtained, passingMarks, totalMarks, full_name, student_attendance, working_days, session.get('class_name'), session.get('semester_name'), path_name, overall_percentage)
    return 
