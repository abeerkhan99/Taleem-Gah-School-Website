from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import psycopg2
import pandas as pd
from pdf import my_pdf

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

# A function that takes in a PostgreSQL query and outputs a pandas database 
def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table
  
# Utilize the create_pandas_table function to create a Pandas data frame
# TAKE USERNAME FROM FRONTEND
username = 'abeer_khan'
info = create_pandas_table("SELECT * FROM faculty WHERE username = '{}'".format(username))

# Close the cursor and connection to so the server can allocate
# bandwidth to other requests
cur.close()
conn.close()

info = list(info.loc[0])
subjects = ['Urdu', 'English', 'Math', 'Social Studies', 'Science', 'Islamiat', 'Sindhi', 'Art Drawing', 'Total Marks']
marksObtained = [11, 89, 9, 12, 92, 93, 5, 75]
passingMarks = [33, 34, 35, 36, 37, 38, 39, 40]
totalMarks = [100, 100, 100, 100, 100, 100, 75, 75]

name = info[1] + " " + info[2]
path = "C://Users//akeel//Desktop//Taleem Gah//Taleem-Gah-School-Website//Code//sig.jpeg"
output_path = 'PDF Reports/test_report.pdf'
pdf = my_pdf(subjects=subjects, marksObtained=marksObtained, passingMarks=passingMarks, totalMarks=totalMarks, name=name, path1=path, path2=path, path3=path, output_path=output_path)
