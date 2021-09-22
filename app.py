import os
import shutil
import csv
import sys
import os
import sqlite3
""" from flask_sqlalchemy import SQLAlchemy """
from flask import Flask,render_template, url_for, flash, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_bootstrap import Bootstrap
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

from flask_mysqldb import MySQL

app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'proj2'
 
mysql = MySQL(app)

bootstrap = Bootstrap(app)
 
 
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html', result={})


@app.route('/program1', methods=["GET"])
def program1():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM User_Account')
	mysql.connection.commit()
	result = cur.fetchall()
	return render_template('program1.html', result=result)

@app.route('/prog1', methods=["POST"])
def prog1():
	IdNo = request.form['IdNo']
	Name = request.form['Name']
	Email = request.form['Email']
	RoleName = request.form['RoleName']
	cur = mysql.connection.cursor()
	sql = " INSERT INTO User_Account VALUES(%s, %s, %s, %s);"
	cur.execute(sql, (IdNo, Name, Email, RoleName,))
	mysql.connection.commit()
	return redirect(url_for("program1"))


@app.route('/program2', methods=["GET"])
def program2():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM User_Roles')
	mysql.connection.commit()
	result = cur.fetchall()
	return render_template('program2.html', result=result)

@app.route('/prog2', methods=["POST"])
def prog2():
	PrivilegeID = request.form['PrivilegeID']
	Role_Description = request.form['Role_Description']
	RoleName = request.form['RoleName']
	cur = mysql.connection.cursor()
	sql = " INSERT INTO User_Roles VALUES(%s, %s, %s)"
	cur.execute(sql, (PrivilegeID, Role_Description, RoleName,))
	mysql.connection.commit()
	return redirect(url_for("program2"))


@app.route('/program3', methods=["GET"])
def program3():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM Tables')
	mysql.connection.commit()
	result = cur.fetchall()
	return render_template('program3.html', result=result)

@app.route('/prog3', methods=["POST"])
def prog3():
	TableName = request.form['TableName']
	IdNo = request.form['IdNo']
	cur = mysql.connection.cursor()
	sql = " INSERT INTO Tables VALUES(%s, %s)"
	cur.execute(sql, (TableName, IdNo,))
	mysql.connection.commit()
	return redirect(url_for("program3"))


@app.route('/program4', methods=["GET"])
def program4():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM Privileges')
	mysql.connection.commit()
	result = cur.fetchall()
	return render_template('program4.html', result=result)

@app.route('/prog4', methods=["POST"])
def prog4():
	PrivilegeID = request.form['PrivilegeID']
	Privilege_Type = request.form['Privilege_Type']
	Privilege_Description = request.form['Privilege_Description']
	cur = mysql.connection.cursor()
	sql = " INSERT INTO Privileges VALUES(%s, %s, %s)"
	cur.execute(sql, (PrivilegeID, Privilege_Type, Privilege_Description,))
	mysql.connection.commit()
	return redirect(url_for("program4"))


@app.route('/program5', methods=["GET"])
def program5():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM (User_Account NATURAL JOIN User_Roles);')
	mysql.connection.commit()
	result = cur.fetchall()
	return render_template('program5.html', result=result)

@app.route('/program6', methods=["GET"])
def program6():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM Privileges NATURAL JOIN User_Roles WHERE Privileges.Privilege_Type = "ACCOUNT";')
	mysql.connection.commit()
	result = cur.fetchall()
	return render_template('program6.html', result=result)


@app.route('/program7', methods=["GET"])
def program7():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM Privileges NATURAL JOIN User_Roles NATURAL JOIN TABLES WHERE Privileges.Privilege_Type = "RELATION";')
	mysql.connection.commit()
	result = cur.fetchall()
	return render_template('program7.html', result=result)


@app.route('/program8', methods=["GET"])
def program8():
	ret = []
	return render_template('program8.html', result=ret)


@app.route('/prog8', methods=["POST"])
def prog8():
	Name = request.form["Name"]
	RoleName = request.form["RoleName"]
	Privilege_Description = request.form["Privilege_Description"]
	cur = mysql.connection.cursor()
	sql = " SELECT * FROM Privileges NATURAL JOIN User_Account NATURAL JOIN User_Roles WHERE Name = (%s) OR RoleName = (%s) OR Privilege_Description = (%s); "
	cur.execute(sql, (Name, RoleName,Privilege_Description))
	mysql.connection.commit()
	result = cur.fetchall()
	return render_template('program8.html', result=result)