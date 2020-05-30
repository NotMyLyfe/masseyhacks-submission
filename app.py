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
    return render_template('healthagency.html')
    
if __name__ == "__main__":
    app.run()