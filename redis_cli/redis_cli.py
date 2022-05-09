from flask import Flask
import redis
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///count_url.db'

db = SQLAlchemy(app)


class CountUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_name = db.Column(db.String(50))
    date = db.Column(db.DateTime)


r = redis.Redis(host='localhost', port=6379, db=10)


@app.route('/', methods=['POST', 'GET'])
def redis_count():
    ip_number = request.remote_addr
    agent = request.user_agent.string
    now = datetime.datetime.now()
    if r.exists(ip_number) == 0:
        url_name = request.base_url
        r.set(ip_number, 1)
        r.expire(ip_number, 5)
        u = CountUrl(url_name=url_name, date=now)
        db.session.add(u)
        db.session.flush()
        db.session.commit()
        return f'посещение {url_name} в {now}'
    else:
        return f'C {ip_number} слишко м часты запрос '


app.run

