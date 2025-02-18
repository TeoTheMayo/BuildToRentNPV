import pandas as pd
import numpy as np 
from flask import Flask, render_template, redirect
import configparser
import requests

#import configuration file
config = configparser.ConfigParser()
config.read("config.conf")

#flask configuration setup
app = Flask(__name__)
app.config["SECRET KEY"] = config["DEFAULT"]["SECRET_KEY"]
app.config["FLASK_ENV"] = config["DEFAULT"]["FLASK_ENV"]
app.config["SQALCHEMY_DATABASE_URI"] = "sqlite://users.sqlite3"
app.config["WTF_CSRF_ENABLED"] = True

#index Route
@app.route('/', methods=["GET", "POST"])
def index():
    return "Hello World"
