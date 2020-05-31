import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session

app = Flask(__name__)
Session(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/healthagency")
def healthagency():
    ip = requests.get(
        "https://api.ipify.org?format=json"
    ).json().get('ip')
    worldInfo = requests.get("https://api.covid19api.com/world/total")
    countryInfo = requests.get(
        'https://api.bigdatacloud.net/data/country-by-ip?ip=' + ip + '&localityLanguage=en&key=bf533feb04e84279b9d098d9a6e5886b'
    ).json()
    return render_template('healthagency.html', countryCode=countryInfo.get('country').get('isoAlpha2'), recovered=worldInfo.get('TotalRecovered'), deaths=worldInfo.get('TotalDeaths'), confirmed=worldInfo.get('TotalConfirmed'))
    
if __name__ == "__main__":
    app.run()