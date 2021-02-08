from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests as request
import time
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)

db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), unique=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, message, timestamp):
        self.message = message
        self.timestamp = timestamp

class MonitorApp:
    def get_users_runner():
        while True:
            date = datetime.utcnow()
            try: 
                res = request.get('http://127.0.0.1:5000/user', headers={"content-type": "application/json"})
                if res.status_code == request.codes.ok:
                    report = Report("Request successful", date)
                else:
                    report = Report("Bad Request", date)
            except:
                report = Report("Service Error", date)
            print(report.message)
            print(f'{report.timestamp}\n')
            db.session.add(report)
            db.session.commit()
            time.sleep(100)

if __name__ == '__main__':
    create_table()
    monitorApp = MonitorApp.get_users_runner()


