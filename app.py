import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import os
from ipaddress import ip_address

app = Flask(__name__)
Session(app)

@app.route("/")
def index():
    worldInfo = requests.get("https://api.covid19api.com/world/total").json()
    return render_template('index.html', recovered=worldInfo.get('TotalRecovered'), deaths=worldInfo.get('TotalDeaths'), confirmed=worldInfo.get('TotalConfirmed'))

@app.route("/healthagency")
def healthagency():
    headers_list = request.headers.getlist("X-Forwarded-For")

    ip = headers_list[0] if headers_list else request.remote_addr

    if ':' in ip:
        ip = ip[:ip.find(':')]
<<<<<<< HEAD
    
=======
>>>>>>> f22cd03ca6f830de6850eb7efcac2c23c17ae645
    if ip_address(ip).is_private:
        ip = requests.get(
        "https://api.ipify.org?format=json"
        ).json().get('ip')
    
    locationData = requests.get(
        'http://api.ipstack.com/' + ip + '?access_key=' + os.getenv('IPSTACK_KEY')
    ).json()
<<<<<<< HEAD
    countryCode = locationData.get('country_code')
    
    arguments = {
        'countryCode' : countryCode
    }

    if countryCode == 'US' or countryCode == 'CA':
        arguments['regionCode'] = locationData.get('region_code')

    return render_template('healthagency.html', **arguments)
    
=======
    print(locationData)
    return render_template('healthagency.html', countryCode=locationData.get('country_code'))
    #, recovered=worldInfo.get('TotalRecovered'), deaths=worldInfo.get('TotalDeaths'), confirmed=worldInfo.get('TotalConfirmed')
>>>>>>> f22cd03ca6f830de6850eb7efcac2c23c17ae645
