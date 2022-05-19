from flask import Flask
import redis
from flask import Flask
from flask import request, make_response
from flask_sqlalchemy import SQLAlchemy
import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///count_url.db'

db = SQLAlchemy(app)


class CountUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_name = db.Column(db.String(50))
    date = db.Column(db.DateTime)


r = redis.Redis(host='localhost', port=6379, db=0)


@app.route('/', methods=['POST', 'GET'])
def redis_index():
    pass


@app.route('/contact', methods=['POST', 'GET'])
def redis_contact():
   pass


@app.before_request
def before_request():
    ip_check = request.remote_addr
    agent = request.user_agent.string
    now = datetime.datetime.now()
    url_name = request.base_url
    cook = request.cookies.items()
    if r.exists(ip_check) == 0:
        r.set(ip_check, 1)
        r.expire(ip_check, 3)
        u = CountUrl(url_name=url_name, date=now)
        print(r.get(ip_check))
        #db.session.add(u)
        #db.session.flush()
        #db.session.commit()
        return 'Статисктика увеличина'
    return 'Слишком много запросов'
app.run()

