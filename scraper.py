import pandas as pd
import numpy as np 
from flask import Flask, render_template, redirect
import configparser
import requests
from bs4 import BeautifulSoup

l=list()
obj={}
target_url = "https://www.zillow.com/homes/for_sale/Los-Angeles-CA_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=buy"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
resp = requests.requests(target_url, headers=headers)

print(resp.status_code)

if __name__ == '__main__':
    print(resp.status_code)