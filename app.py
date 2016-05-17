# app.py
import os

from flask import Flask
from micawber import bootstrap_basic
from peewee import SqliteDatabase

from flask import render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from distraqt_database_setup import Base	

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# from database_setup import Base, Restaurant, MenuItem, User

# Connect to Database and create database session
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

app = Flask(__name__)

# APP_ROOT = os.path.dirname(os.path.realpath(__file__))
# DATABASE = os.path.join(APP_ROOT, 'notes.db')
# DEBUG = False

# app = Flask(__name__)
# app.config.from_object(__name__)
# db = SqliteDatabase(app.config['DATABASE'], threadlocals=True)
# oembed = bootstrap_basic()


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)