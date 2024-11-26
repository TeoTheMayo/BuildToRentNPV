import pandas as pd
import numpy as np 
from flask import Flask, render_template, redirect
import configparser
import requests
from bs4 import BeautifulSoup

#establsh headers
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}

r = requests.get("https://www.zillow.com/homedetails/590-Ocean-Dr-APT-8C-Key-Biscayne-FL-33149/44034282_zpid/", headers=headers)
statCode = str(r.status_code)
soup = BeautifulSoup(r.content, features="html.parser")

#find something
#for link in soup.find_all('a'):
#    print(link.get('href'))


if __name__ == '__main__':
    print(statCode)
    print(soup.prettify())