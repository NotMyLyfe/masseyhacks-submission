import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import os
from ipaddress import ip_address
import json

app = Flask(__name__)
Session(app)

@app.route("/")
def index():
    worldInfo = requests.get("https://api.covid19api.com/world/total").json()
    return render_template('index.html', recovered=worldInfo.get('TotalRecovered'), deaths=worldInfo.get('TotalDeaths'), confirmed=worldInfo.get('TotalConfirmed'))
@app.route("about")
def about():
    return render_template('about.html')

@app.route("/healthagency")
def healthagency():
    headers_list = request.headers.getlist("X-Forwarded-For")

    ip = headers_list[0] if headers_list else request.remote_addr

    if ':' in ip:
        ip = ip[:ip.find(':')]
    
    if ip_address(ip).is_private:
        ip = requests.get(
        "https://api.ipify.org?format=json"
        ).json().get('ip')
    
    locationData = requests.get(
        'http://api.ipstack.com/' + ip + '?access_key=' + os.getenv('IPSTACK_KEY')
    ).json()
    countryCode = locationData.get('country_code')
    
    with open('healthAgencies.json', 'r') as file:
        healthAgencies = json.load(file)

    arguments = {}

    if countryCode == 'US' or countryCode == 'CA':
        arguments['national'] = healthAgencies[countryCode]['nationalHealthAgency']
        arguments['regional'] = healthAgencies[countryCode]['regionalHealthAgencies'][locationData.get('region_code')]

    return render_template('healthagency.html', **arguments)
    
