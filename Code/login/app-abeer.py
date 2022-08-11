from pickletools import read_uint1
from flask import Flask, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL, create_engine
from sqlalchemy.orm import Session
import os
import psycopg2

# app instance
app = Flask(__name__, template_folder='templates')
# for sessions
app.secret_key = 'BAD_SECRET_KEY'

def get_db_connection():
    conn = psycopg2.connect(
            host="localhost",
            database="taleem-gah",
            user= "postgres",
            password= "akeelmedina",
            port = "5432")

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
            cur.execute('SELECT Username from faculty where Username = %s', (user_name,))
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
                    session['user_info_email'] = user_object_string
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
        faculty_cnic = request.form['cnic']
        faculty_address = request.form['home_address']
        faculty_username = request.form['u_name']
        faculty_email = request.form["email_a"]
        faculty_password = request.form['pass']
        faculty_phone_number = request.form['phone_no']
        faculty__type = request.form['f_type']

        # print(faculty_first_name)
        # print(faculty_last_name)
        # print(faculty_cnic)
        # print(faculty_address)
        # print(faculty_username)
        # print(faculty_email)
        # print(faculty_password)
        # print(faculty_phone_number)
        # print(faculty__type)
        
        # check if CNIC exists
        cur.execute('SELECT CNIC from faculty where CNIC = %s', (faculty_cnic,))
        faculty_cnic_object = cur.fetchall()

        print("NAME IS:", faculty_cnic_object)

        # check if username exists
        cur.execute('SELECT Username from faculty where Username = %s', (faculty_username,))
        faculty_username_object = cur.fetchall()

        print("NAME IS:", faculty_username_object)

        # check if email exists
        cur.execute('SELECT Email from faculty where Email = %s', (faculty_email,))
        faculty_email_object = cur.fetchall()

        print("NAME IS:", faculty_email_object)

        if len(faculty_cnic_object) != 0 or len(faculty_username_object) != 0 or len(faculty_email_object) != 0:
            if len(faculty_cnic_object) != 0:
                return render_template('register.html', message = "An account with this CNIC already exists. Please enter a different CNIC number.")
        
            elif len(faculty_username_object) != 0:
                return render_template('register.html', message = "This username has already been taken. Please enter a different username.")

            elif len(faculty_email_object) != 0:
                return render_template('register.html', message = "An account with this email already exists. Please enter a different email.")
            
            elif len(faculty_cnic_object) != 0 and len(faculty_username_object) != 0:
                return render_template('register.html', message = "An account with this CNIC and username already exists.")

            elif len(faculty_cnic_object) != 0 and len(faculty_email_object) != 0:
                return render_template('register.html', message = "An account with this CNIC and email already exists.")
            
            elif len(faculty_username_object) != 0 and len(faculty_email_object) != 0:
                return render_template('register.html', message = "An account with this username and email already exists.")
        
        elif len(faculty_cnic_object) != 0 and len(faculty_username_object) != 0 and len(faculty_email_object) != 0:
            return render_template('register.html', message = "An account with this CNIC, username, and email already exists.")

        else:
            # insert information into database
            cur.execute("INSERT INTO faculty(FirstName, LastName, CNIC, Address, Username, Email, Pass, PhoneNo, faculty_type) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s)", 
                        (faculty_first_name, faculty_last_name, faculty_cnic, faculty_address, faculty_username, faculty_email, faculty_password, faculty_phone_number, faculty__type,))

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
        user_email = request.form['u_email']
        user_cnic = request.form['u_cnic']

        cur.execute('SELECT CNIC from faculty where CNIC = %s and Email = %s', (user_cnic, user_email,))
        user_email_object = cur.fetchall()

        cur.execute('SELECT Email from faculty where CNIC = %s and Email = %s', (user_cnic, user_email,))
        user_cnic_object = cur.fetchall()

        # check if email and cnic exists 
        if len(user_email_object) != 0 and len(user_cnic_object) != 0:

            user_email_item = user_email_object.pop()
            user_email_string = ''.join(user_email_item)

            user_cnic_item = user_cnic_object.pop()
            user_cnic_string = ''.join(user_cnic_item)

            session['reset_u_email'] = user_email_string
            session['reset_u_cnic'] = user_cnic_string

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
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_email')) != 0:

        if request.method == 'POST':
            user_new_pass = request.form['new_pass']

            # alter table details
            cur.execute("UPDATE faculty SET Pass = %s WHERE CNIC = %s AND Email = %s", (user_new_pass, session.get('reset_u_cnic'), session.get('reset_u_email'),))
            
            # save changes to database
            conn.commit()

            # clear session data
            session.pop('reset_u_cnic', default=None)
            session.pop('reset_u_email', default=None)

            return render_template('reset-pass.html', message = "Password changed. You may log in now with the new password.")
    else:
        return redirect(url_for('verify'))


@app.route('/admin-homepage')
def admin_homepage():
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_email')) != 0 and session.get('user_info_type') == 'Admin':
        return render_template('admin-homepage.html')
    else:
        return redirect(url_for('login'))

@app.route('/teacher-homepage')
def teacher_homepage():
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_email')) != 0 and session.get('user_info_type') == 'Teacher':
        return render_template('admin-homepage.html')
    else:
        return render_template('login')


@app.route('/generate-report-card')
def student_report():
    return render_template('student-report-card.html')
    # return 'Hello World!'


@app.route('/generate-financial-sheet')
def financial_sheet():
    return render_template('financial-sheet.html')
    # return 'Hello World!'


@app.route('/view-records')
def view_records_homepage():
    return render_template('view_records_admin_homepage.html')
    # return 'Hello World!'

@app.route('/faculty-records')
def display_faculty_records():
    #extract all faculty info from database
    #store in list
    if len(session.get('user_info_name')) != 0 and len(session.get('user_info_email')) != 0 and session.get('user_info_type') == 'Admin':
        
        cur.execute('SELECT facultyID, FirstName, LastName, CNIC, Address, Username, Email, PhoneNo, faculty_type from faculty')
        faculty_records_object = cur.fetchall()
        print('FACULTY RECORDS ARE:', faculty_records_object)
        
        return render_template('view_faculty_records.html', len = len(faculty_records_object), faculty_records_object = faculty_records_object)
    else:
        return redirect(url_for('login', message = "Please login."))


@app.route('/student-records')
def display_student_records():
    #extract all faculty info from database
    #store in list

    item_list = ['item1', 'item2', 'item3'] # Up to 1000 items
    
    return render_template('view_student_records.html', item_list=item_list)


if __name__ == '__main__':
    app.run()
