from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pars_data.db'
login = LoginManager(app)

login.login_view = '/login'
db = SQLAlchemy(app)


bootstrap = Bootstrap(app)
