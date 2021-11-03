import mysql.connector as mysql
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search
import smtplib
 
import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
 
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag
from uuid import uuid4
import yaml
from db_connection import get_database_connection

st.set_page_config(
    page_title="Admission Form",
    page_icon=":sunny:",
    # layout="wide",
    initial_sidebar_state="expanded",
)
# database localhost connection
# @st.cache()

# def get_database_connection():
#     db = mysql.connect(host = "localhost",
#                       user = "root",
#                       passwd = "root",
#                       database = "mydatabase",
#                       auth_plugin='mysql_native_password')
#     cursor = db.cursor()
#     return cursor, db
 
cursor, db = get_database_connection()
 
# cursor.execute("SHOW DATABASES")
 
# databases = cursor.fetchall() ## it returns a list of all databases present
 
# st.write(databases)
 
# cursor.execute('''CREATE TABLE information (id varchar(255),
#                                               studentname varchar(255),address varchar(255),
#                                               re_date date,
# 												status varchar(255))''')
# cursor.execute("Select * from information")
# tables = cursor.fetchall()
# st.write(tables)

def admin():
    username=st.sidebar.text_input('Username',key='user')
    password=st.sidebar.text_input('Password',type='password',key='pass')
    st.session_state.login=st.sidebar.checkbox('Login')

    if st.session_state.login==True:
        if username=="hamid" and password=='hamid':
            st.sidebar.success('You are Login Successfully!')
            infor = st.sidebar.selectbox('Select One', ['......', 'Information'])
            if infor=='Information':
                id = st.text_input('Tracking Code')
                Submit = st.button(label='Search')
                if Submit:
                    cursor.execute(f"select * from information where id='{id}'")
                    tables = cursor.fetchall()
                    st.write(tables)

            date1=st.date_input('Date1')
            date2=st.date_input('Date2')
            cursor.execute(f"select * from information where re_date between '{date1}' and '{date2}'")
            # db.commit()
            tables =cursor.fetchall()
            # st.write(tables)
            for i in tables:
                st.subheader(f"All information of {i[1]}")
                st.write(f"Tracking id :-{i[0]}")
                st.write(f"Name :-{i[1]}")
                st.write(f"Date :-{i[2]}")
                st.write(f"Current Status :-{i[3]}")
                st.write(f"Address :-{i[4]}")
                st.write(f"Father's Name :-{i[5]}")
                st.write(f"Mother's Name :-{i[6]}")
                st.write(f"Email :-{i[7]}")
                st.write(f"Gender :-{i[8]}")
                Accept=st.button('Accept',key=i[0])
                if Accept:
                     st.write('Accepted')
                     cursor.execute(f"Update information set status='Accepted' where id='{i[0]}'")
                     db.commit()
                Reject=st.button('Reject',key=i[0])
                if Reject:
                     st.write('Rejected')
                     cursor.execute(f"Update information set status='Rejected' where id='{i[0]}'")
                     db.commit()


        else:
            st.sidebar.warning('Username or Password does not match!!')


def form():
    id=uuid4()
    id=str(id)[:10]
    with st.form(key='member form'):
        st.subheader('Registration Form')
        sname=st.text_input('Student Name')
        fname=st.text_input(f"Father's Name")
        mname=st.text_input(f"Mother's Name")
        address=st.text_input('Address')
        email=st.text_input('Email')
        gender=st.radio('Select Gender',['Male','Female','Others'])
        re_date=st.date_input('Registration Date')
        status='In Progress'
        if st.form_submit_button('Submit'):
            query = f'''INSERT INTO information (id,studentname,re_date,status,address,fname,mname,email,gender
                                ) VALUES ('{id}','{sname}','{re_date}','{status}','{address}','{fname}','{mname}','{email}','{gender}'
                                                )'''
            cursor.execute(query)
            db.commit()
            st.success(f'Congratulation *{sname}*! You have successfully Registered')
            st.code(id)
            st.warning("Please Store this code!!!")

def info():
    id=st.text_input('Your Code')
    Submit=st.button(label='Search')
    if Submit:
    	cursor.execute(f"select * from information where id='{id}'")
    	tables = cursor.fetchall()
    	st.write(tables)

def stat():
    st.subheader('Check Status')
    id=st.text_input('Enter your Tracking ID: ')
    submit=st.button('Search',key='sub')
    if submit:
        cursor.execute(f"Select * from information where id='{id}'")
        table=cursor.fetchall()
        if table[0][3]=='Accepted':
            st.info('Congratulations! You are accepted.')
        elif table[0][3]=='Rejected':
            st.warning('Sorry! You are rejected.')
        else:
            st.info('In Progress...')

def main():
    st.title('Diploma in Data Science Admission Portal')
    st.header('International Islamic University Chittagong')
    selected=st.sidebar.selectbox('Select',
                        ('-----------',
                        'Admin',
                        'Registration',
                        'Status'
                        ))
    if selected=='Admin':
        admin()
    elif selected=='Registration':
        form()
    elif selected=='Information':
        info()
    elif selected=='Status':
        stat()
if __name__=='__main__':
    main()
