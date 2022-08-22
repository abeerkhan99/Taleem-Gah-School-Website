from pickletools import read_uint1
from flask import Flask, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL, create_engine, delete
from sqlalchemy.orm import Session
import os
import psycopg2

# app instance
app = Flask(__name__, template_folder='templates')
# for sessions
app.secret_key = 'BAD_SECRET_KEY'

def get_db_connection():
    conn = psycopg2.connect(
                    host="ec2-99-81-137-11.eu-west-1.compute.amazonaws.com",
                    database="daa4fhosr8e8gk",
                    user= 'wwaakwjbwwkzsz',
                    password= '8f8d7d62bfbd038bc9501b2bd87f7a7bd73625737c94e86c106dfeb8040e3397',
                    port = 5432)
    return conn

# Open a cursor to perform database operations
conn = get_db_connection()
cur = conn.cursor()

# routing
@app.route('/')
def home():
    return render_template('welcome.html')
    # return 'Hello World!'

@app.route('/login')
def login():
    return render_template('login.html')
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
            try:
                cur.execute('SELECT Username from faculty where Username = %s', (user_name,))
            except psycopg2.InterfaceError as exc:
                print(exc.message)
                conn = psycopg2.connect(
                    host="ec2-99-81-137-11.eu-west-1.compute.amazonaws.com",
                    database="daa4fhosr8e8gk",
                    user= 'wwaakwjbwwkzsz',
                    password= '8f8d7d62bfbd038bc9501b2bd87f7a7bd73625737c94e86c106dfeb8040e3397',
                    port = 5432)
                cursor = conn.cursor()
            user_object = cur.fetchall() 
            user_object_string = None

            #make user_object into string
            if user_object != []:
                user_object_item = user_object.pop()
                user_object_string = ''.join(user_object_item)

            # if username exists, then check password and username combo 
            if user_object_string != user_name:
                return render_template('login.html', message = "This username does not exist")

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
                    return render_template('login.html', message = "Incorrect Password!")
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
    return render_template('login.html')
    # return 'Hello World!'

@app.route('/registration')
def register():
    return render_template('register.html')

@app.route('/registration-submit', methods = ['GET', 'POST'])
def registration_submit():

    if request.method == 'POST':
        faculty_first_name = request.form['f_name']
        faculty_last_name = request.form['l_name']
        faculty_username = request.form['u_name']
        faculty_password = request.form['pass']
        faculty_phone_number = request.form['phone_no']
        faculty__type = request.form['f_type']
        
        # check if username exists
        cur.execute('SELECT Username from faculty where Username = %s', (faculty_username,))
        faculty_username_object = cur.fetchall()

        # check if phone number exists
        cur.execute('SELECT PhoneNo from faculty where Username = %s', (faculty_phone_number,))
        faculty_number_object = cur.fetchall()

        if len(faculty_username_object) != 0 or len(faculty_number_object) != 0:
            if len(faculty_username_object) != 0:
                return render_template('register.html', message = "This username has already been taken. Please enter a different username.")

            elif len(faculty_number_object) != 0:
                return render_template('register.html', message = "An account with this number already exists. Please enter a different email.")

        elif len(faculty_username_object) != 0 and len(faculty_number_object) != 0:
            return render_template('register.html', message = "An account with this username and phone number already exists.")

        else:
            # insert information into database
            cur.execute("INSERT INTO faculty(FirstName, LastName, Username, Pass, PhoneNo, faculty_type) VALUES(%s,%s, %s, %s, %s, %s,", 
                        (faculty_first_name, faculty_last_name, faculty_username, faculty_password, faculty_phone_number, faculty__type,))

            conn.commit()
            # return render_template('register.html', message = "An account has been created. Please log in now.")
            return redirect(url_for('login', message = "An account has been created. Please log in now."))
    return 

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


@app.route('/generate-report-card', methods = ['GET', 'POST'])
def student_report():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        
        cur.execute('SELECT class_name from classes')
        list_of_classes = cur.fetchall()

        return render_template('student-report-card.html', grade = list_of_classes )
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/grade-submit', methods = ['GET', 'POST'])
def grade_selector():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_email')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
    
        select = request.form.get('grade_select')

        return render_template('report-card-form.html', select = str(select))
    else:
        return redirect(url_for('login', message = "Please login."))




@app.route('/generate-financial-sheet')
def financial_sheet():
    return render_template('financial-sheet.html')
    # return 'Hello World!'

# ADMIN WORK
@app.route('/view-records')
def view_records_homepage():
    return render_template('view_records_admin_homepage.html')
    # return 'Hello World!'

@app.route('/faculty-records')
def display_faculty_records():
    #extract all faculty info from database
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0 and session.get('user_info_type') == 'Admin':
        
        cur.execute('SELECT facultyID, FirstName, LastName, Username, PhoneNo, faculty_type  from faculty ORDER BY faculty_type ASC')
        faculty_records_object = cur.fetchall()
        # print('FACULTY RECORDS ARE:', faculty_records_object)

        # attempting to add classes and subjects to show them in view page
        cur.execute('SELECT facultyID, teacher_subjectName from teacher_has_subject, faculty where facultyID = teacher_facultyID')
        subject_records_object = cur.fetchall()

        faculty_record_list = compile_faculty_record(faculty_records_object, subject_records_object)
        
        # return render_template('view_faculty_records.html', len = len(faculty_records_object), faculty_records_object = faculty_records_object)
        return render_template('view_faculty_records.html', len = len(faculty_record_list), faculty_records_object = faculty_record_list)

    else:
        return redirect(url_for('login', message = "Please login."))


def compile_faculty_record(faculty_records_object, subject_records_object):
    faculty_record_list = []
    for x in faculty_records_object:
        l = []
        for i in x:
            l.append(i)
        s = []
        for y in subject_records_object:
            if x[0] == y[0]:
                s.append(y[1])
        if len(s) == 0:
            l.append("None")
        else:
            l.append(s)
        faculty_record_list.append(l)

    return faculty_record_list



@app.route('/edit_faculty_record', methods = ['GET', 'POST'])
def edit_faculty_records():
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0 and session.get('user_info_type') == 'Admin':
        if request.method == 'POST':
            
            cur.execute('SELECT facultyID, FirstName, LastName, Username, PhoneNo, faculty_type from faculty')
            faculty_records_object = cur.fetchall()
            # print('FACULTY RECORDS ARE:', faculty_records_object)

            cur.execute('SELECT facultyID, teacher_subjectName from teacher_has_subject, faculty where facultyID = teacher_facultyID')
            subject_records_object = cur.fetchall()

            faculty_record_list = compile_faculty_record(faculty_records_object, subject_records_object)

            # store information of record to edit
            edit_item = []
            for x in range(len(faculty_record_list[0])):
                edit_item.append(request.form[str(x)])
            print(edit_item)

            session['edit_record'] = edit_item
            
            cur.execute('SELECT count(subjectName) from subject')
            total_subjects_object = cur.fetchall()
            
            return render_template('edit-faculty-records.html', edit_item = edit_item, subject_count = int(total_subjects_object[0]), len = len(edit_item[len(edit_item)-1]) - 1)
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/edit_faculty_record_submit', methods = ['GET', 'POST'])
def edit_faculty_records_submit():
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0 and session.get('user_info_type') == 'Admin':
        if request.method == 'POST':

            # new info submitted
            new_edit_item = []
            for x in range(1, len(session.get('edit_record'))):
                new_edit_item.append(request.form[str(x)])
            print(new_edit_item)

            # compare new details and old details of record
            old_edit_item = session.get('edit_record')

            if new_edit_item == old_edit_item:
                print("no changes detected")

                cur.execute('SELECT facultyID, FirstName, LastName, Username, PhoneNo, faculty_type from faculty')
                faculty_records_object = cur.fetchall()
        
                return render_template('view_faculty_records.html', len = len(faculty_records_object), faculty_records_object = faculty_records_object)
                
            elif new_edit_item != old_edit_item:

                cur.execute('SELECT Username from faculty where CNIC = %s', (new_edit_item[3],))
                compare_name_object = cur.fetchall()

                cur.execute('SELECT PhoneNo from faculty where Username = %s', (new_edit_item[4],))
                compare_number_object = cur.fetchall()

                if len(compare_name_object) != 0 or len(compare_number_object) != 0:
                    if len(compare_name_object) != 0:
                        return render_template('edit-faculty-records.html', edit_item = new_edit_item, message = "This username has already been taken. Please enter a different username.")
                
                    elif len(compare_number_object) != 0:
                        return render_template('edit-faculty-records.html', edit_item = new_edit_item, message = "An account with this phone number already exists. Please enter a different number.")

                    elif len(compare_name_object) != 0 and len(compare_number_object) != 0:
                        return render_template('edit-faculty-records.html', edit_item = new_edit_item, message = "An account with this Username and phone number already exists.")
                else:
                    # update information into database
                    cur.execute("UPDATE faculty SET FirstName = %s and LastName = %s and CNIC = %s Username = %s and PhoneNo = %s and faculty_type = %s WHERE Username = %s AND PhoneNo = %s", 
                                (new_edit_item[1], new_edit_item[2], new_edit_item[3], new_edit_item[4], new_edit_item[5], old_edit_item[3], old_edit_item[4],))

                    conn.commit()
                    cur.execute('SELECT facultyID, FirstName, LastName, Username, PhoneNo, faculty_type from faculty')
                    faculty_records_object = cur.fetchall()
        
                    return render_template('view_faculty_records.html', len = len(faculty_records_object), faculty_records_object = faculty_records_object)
    else:
        return redirect(url_for('login', message = "Please login."))

    

@app.route('/delete_faculty_records', methods = ['GET', 'POST'])
def delete_faculty_records():
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0 and session.get('user_info_type') == 'Admin':
        if request.method == 'POST':
            
            cur.execute('SELECT facultyID, FirstName, LastName, Username, PhoneNo, faculty_type from faculty')
            frecords_object = cur.fetchall()
            # print('FACULTY RECORDS ARE:', faculty_records_object)

            # get information to delete from the database
            delete_item = []
            for x in range(len(frecords_object[0])):
                delete_item.append(request.form[str(x)])
            print(delete_item)

            cur.execute('DELETE from faculty WHERE facultyID = %s AND FirstName = %s AND LastName = %s AND Username = %s AND PhoneNo = %s AND faculty_type = %s'
                        (delete_item[0], delete_item[1], delete_item[2], delete_item[3], delete_item[4], delete_item[5],))
            
            # reset sequence
            cur.execute('ALTER SEQUENCE faculty_facultyID_seq RESTART WITH 1')

            conn.commit()

            cur.execute('SELECT facultyID, FirstName, LastName, Username, PhoneNo, faculty_type from faculty')
            faculty_records_object = cur.fetchall()

            return render_template('view_faculty_records.html', len = len(faculty_records_object), faculty_records_object = faculty_records_object, message = "Deletion Successful")
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/add-record', methods = ['GET', 'POST'])
def admin_add_records_homepage():
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0 and session.get('user_info_type') == 'Admin':
        return render_template('admin-add-record-homepage.html')
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/add-faculty-record', methods = ['GET', 'POST'])
def add_faculty_records():
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0 and session.get('user_info_type') == 'Admin':
        return render_template('add-faculty-record.html')
    else:
        return redirect(url_for('login', message = "Please login."))

@app.route('/add-faculty-record-submit', methods = ['GET', 'POST'])
def add_faculty_record_submit():
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0 and session.get('user_info_type') == 'Admin':
        if request.method == 'POST':
            faculty_first_name = request.form['f_name']
            faculty_last_name = request.form['l_name']
            faculty_username = request.form['u_name']
            faculty_password = request.form['pass']
            faculty_phone_number = request.form['phone_no']
            faculty__type = request.form['f_type']
            
            # check if username exists
            cur.execute('SELECT Username from faculty where Username = %s', (faculty_username,))
            faculty_username_object = cur.fetchall()

            # check if number exists
            cur.execute('SELECT PhoneNo from faculty where Email = %s', (faculty_phone_number,))
            faculty_number_object = cur.fetchall()

            if len(faculty_username_object) != 0 or len(faculty_number_object) != 0:
                
                if len(faculty_username_object) != 0:
                    return render_template('add-faculty-record.html', message = "This username has already been taken. Please enter a different username.")

                elif len(faculty_number_object) != 0:
                    return render_template('add-faculty-record.html', message = "An account with this phone number already exists. Please enter a different phone number.")
                
                elif len(faculty_username_object) != 0 and len(faculty_number_object) != 0:
                    return render_template('add-faculty-record.html', message = "An account with this username and phone number already exists.")
            else:
                # insert information into database
                cur.execute("INSERT INTO faculty(FirstName, LastName, Username, Pass, PhoneNo, faculty_type) VALUES(%s,%s, %s, %s, %s, %s)", 
                            (faculty_first_name, faculty_last_name,faculty_username,faculty_password, faculty_phone_number, faculty__type,))

                conn.commit()
                return redirect(url_for('add_faculty_records', message = "Faculty added! Would you like to add more?"))
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/student-records')
def display_student_records():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        
        cur.execute('SELECT studentID, FirstName, LastName, Gender from student')
        student_records_object = cur.fetchall()
        
        return render_template('view_student_records.html', len = len(student_records_object), student_records_object = student_records_object)
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/edit_student_record', methods = ['GET', 'POST'])
def edit_student_records():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):

        if request.method == 'POST':
            
            cur.execute('SELECT studentID, FirstName, LastName, Gender from student')
            student_records_object = cur.fetchall()
        
            # store info to edit
            edit_item = []
            for x in range(len(student_records_object[0])):
                edit_item.append(request.form[str(x)])
            print(edit_item)

            session['edit_student_record'] = edit_item
            
            return render_template('edit-student-records.html', edit_item = edit_item)
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/edit_student_record_submit', methods = ['GET', 'POST'])
def edit_student_records_submit():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        if request.method == 'POST':

            # new info to add in the database
            new_edit_item = []
            for x in range(1, len(session.get('edit_student_record'))):
                new_edit_item.append(request.form[str(x)])
            print(new_edit_item)

            # compare new details and old details of record
            old_edit_item = session.get('edit_student_record')

            if new_edit_item == old_edit_item:
                print("no changes detected")

                cur.execute('SELECT studentID, FirstName, LastName, Gender, from student')
                student_records_object = cur.fetchall()
        
                return render_template('view_student_records.html', len = len(student_records_object), student_records_object = student_records_object)
                
            # records can be similar (same student names)
            elif new_edit_item != old_edit_item:

                if new_edit_item[1] != old_edit_item[1]:
                    # check if student name already exists in the database or not
                    cur.execute('SELECT FirstName from student where FirstName = %s and LastName = %s', (new_edit_item[1], new_edit_item[2]))
                    student_first_name_object = cur.fetchall()

                    cur.execute('SELECT LastName from student where FirstName = %s and LastName = %s', (new_edit_item[1], new_edit_item[2],))
                    student_last_name_object = cur.fetchall()

                    if len(student_first_name_object) != 0 and len(student_last_name_object) != 0:
                        cur.execute('SELECT repetition from student WHERE FirstName = %s AND LastName = %s', (new_edit_item[1], new_edit_item[2],))
                        student_repetition_object = cur.fetchall()
                        print("REPETITIOn IS:", student_repetition_object)

                        # add repetition
                        if len(student_repetition_object) != 0:
                            repetition_item = int(student_repetition_object[len(student_repetition_object)-1][0])
                            new_repetition_item = repetition_item + 1

                            #update database
                            cur.execute("UPDATE student SET FirstName = %s and LastName = %s and Gender = %s and repetition = %s WHERE studentID = %s", 
                                        (new_edit_item[1], new_edit_item[2], new_edit_item[3], str(new_repetition_item), old_edit_item[0],))
                            conn.commit()

                        elif len(student_repetition_object) == 0:
                            cur.execute("UPDATE student SET FirstName = %s and LastName = %s and Gender = %s and repetition = %s WHERE studentID = %s", 
                                        (new_edit_item[1], new_edit_item[2], new_edit_item[3], '1', old_edit_item[0],))
                            conn.commit()

                elif new_edit_item[1] == old_edit_item[1]:
                    cur.execute("UPDATE student SET FirstName = %s and LastName = %s and Gender = %s and repetition = %s WHERE studentID = %s", 
                            (new_edit_item[1], new_edit_item[2], new_edit_item[3], '1', old_edit_item[0],))
                    conn.commit()
     
            cur.execute('SELECT studentID, FirstName, LastName, DOB, Guardian_FirstName, Guardian_LastName, Guardian_NIC, Guardian_Number, Address, CNIC, Gender, Nationality from student')
            student_records_object = cur.fetchall()

            return render_template('view_student_records.html', len = len(student_records_object), student_records_object = student_records_object)
        
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/delete_student_records', methods = ['GET', 'POST'])
def delete_student_records():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        if request.method == 'POST':
            
            cur.execute('SELECT studentID, FirstName, LastName, DOB, Guardian_FirstName, Guardian_LastName, Guardian_NIC, Guardian_Number, Address, CNIC, Gender, Nationality from student')
            srecords_object = cur.fetchall()
        

            delete_item = []
            for x in range(len(srecords_object[0])):
                delete_item.append(request.form[str(x)])
            print(delete_item)

            cur.execute('DELETE from student WHERE studentID = %s AND FirstName = %s AND LastName = %s DOB = %s and Guardian_FirstName = %s and Guardian_LastName = %s and Guardian_NIC = %s and Guardian_Number = %s and Address = %s and CNIC = %s and Gender = %s and Nationality = %s'
                        (delete_item[0], delete_item[1], delete_item[2], delete_item[3], delete_item[4], delete_item[5], delete_item[6], delete_item[7], delete_item[8], delete_item[9], delete_item[10], delete_item[11],))
            
            # reset sequence
            cur.execute('ALTER SEQUENCE student_studentID_seq RESTART WITH 1')

            conn.commit()

            
            cur.execute('SELECT studentID, FirstName, LastName, DOB, Guardian_FirstName, Guardian_LastName, Guardian_NIC, Guardian_Number, Address, CNIC, Gender, Nationality from student')
            student_records_object = cur.fetchall()

            return render_template('view_student_records.html', len = len(student_records_object), student_records_object = student_records_object)
    else:
        return redirect(url_for('login', message = "Please login."))



@app.route('/add-student-record', methods = ['GET', 'POST'])
def add_student_records():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):
        return render_template('add-student-record.html')
    else:
        return redirect(url_for('login', message = "Please login."))

@app.route('/add-student-record-submit', methods = ['GET', 'POST'])
def add_student_record_submit():
    if (len(session.get('user_info_name')) != 0 and len(session.get('user_info_username')) != 0) and (session.get('user_info_type') == 'Admin' or session.get('user_info_type') == 'Teacher'):

        if request.method == 'POST':
            student_first_name = request.form['f_name']
            student_last_name = request.form['l_name']
            student_gender = request.form['gender']
            
            # check if student first name exists
            cur.execute('SELECT FirstName from student where FirstName = %s and LastName = %s', (student_first_name, student_last_name))
            student_first_name_object = cur.fetchall()

            # check if student last name exists
            cur.execute('SELECT LastName from student where FirstName = %s and LastName = %s', (student_first_name, student_last_name,))
            student_last_name_object = cur.fetchall()

            if len(student_first_name_object) != 0 and len(student_last_name_object) != 0:
                # insert into database with repetition
                cur.execute('SELECT repetition from student where FirstName = %s and LastName = %s', (student_first_name, student_last_name,))
                student_repetition_object = cur.fetchall()
                if len(student_repetition_object) != 0:
                    repetition_item = int(student_repetition_object[len(student_repetition_object)-1][0])
                    new_repetition_item = repetition_item + 1

                cur.execute("INSERT INTO student(FirstName, LastName, Gender, repetition) VALUES(%s,%s, %s, %s)", 
                            (student_first_name, student_last_name, student_gender, str(new_repetition_item),))

                conn.commit()
                return redirect(url_for('add_student_records', message = "Student added! Would you like to add more?"))
            else:
                # insert information into database
                cur.execute("INSERT INTO student(FirstName, LastName, Gender, repetition) VALUES(%s,%s, %s, %s)", 
                            (student_first_name, student_last_name, student_gender, '1',))

                conn.commit()
                return redirect(url_for('add_student_records', message = "Student added! Would you like to add more?"))
    else:
        return redirect(url_for('login', message = "Please login."))




if __name__ == '__main__':
    app.run()
