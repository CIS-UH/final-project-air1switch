import hashlib
import flask
import mysql.connector
from flask import request, jsonify, make_response

# create app
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# connect to AWS database
db = mysql.connector.connect(
    host="cis2368-database.c1oqo2o88zpa.us-east-2.rds.amazonaws.com",   # AWS endpoint link
    user="admin",           # username
    password="eaortiz6",    # password
    database="ticketsystem" # database name
)
