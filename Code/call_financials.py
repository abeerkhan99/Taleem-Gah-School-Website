from flask import Flask, render_template, url_for, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
import psycopg2
import pandas as pd
import financials
import datetime


# def get_db_connection():
#     conn = psycopg2.connect(
#             host="localhost",
#             database="taleem-gah",
#             user= "postgres",
#             password= "akeelmedina",
#             port = "5432")

#     return conn

# # Open a cursor to perform database operations
# conn = get_db_connection()
# cur = conn.cursor()

# # A function that takes in a PostgreSQL query and outputs a pandas database 
# def create_pandas_table(sql_query, database = conn):
#     table = pd.read_sql_query(sql_query, database)
#     return table
  
# # Utilize the create_pandas_table function to create a Pandas data frame
# # Store the data as a variable
# vendor_info = create_pandas_table("SELECT * FROM faculty")
# vendor_info

# # Close the cursor and connection to so the server can allocate
# # bandwidth to other requests
# cur.close()
# conn.close()


f = open('financials.csv', 'w+')
f.close()
financials.main('add', [datetime.datetime.today(), 'Donor 1', 1000])
financials.main('add', [datetime.datetime.today(), 'Donor 2', 100])
financials.main('add', [datetime.datetime(2001, 1, 12), 'Donor 3', 200])
financials.main('add', [datetime.datetime(2001, 1, 12), 'Donor 5', 300])
financials.main('add', [datetime.datetime.today(), 'Donor 7', 10000])

financials.main('update', [datetime.datetime.today(), 'Donor 2', 100, 'Donor 11', 1])

print(financials.main('get', [datetime.datetime.today()]))
print(financials.main('total', [datetime.datetime.today()]))


# dbschema ='myschema'
# engine = create_engine('postgresql://XX:YY@localhost:5432/DB', 
#                        connect_args={'options': '-csearch_path={}'.format(dbschema )})

# df =  psql.read_sql('Select * from myschema."df"', con = engine)