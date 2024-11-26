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

#establsh headers
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}

#index Route
@app.route('/', methods=["GET", "POST"])
def index():
    r = requests.get("https://www.realtor.com/realestateandhomes-detail/149-3rd-Ave_San-Francisco_CA_94118_M16017-14990", headers=headers)
    statCode = str(r.status_code)
    return r.content()
