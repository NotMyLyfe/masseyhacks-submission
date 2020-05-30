import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session

app = Flask(__name__)
Session(app)

@app.route("/")
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run()