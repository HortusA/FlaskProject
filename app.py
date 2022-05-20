from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from nris import bp_nris
from elastic.el_search import bp_elastic
from leads_id.leads import bp_leads
from parser_art.pars_article import bp_pars
from user_login_panel.login_user import bp_admin
from flask_login import LoginManager


app = Flask(__name__)
app.register_blueprint(bp_nris, url_prefix='/nris')
app.register_blueprint(bp_elastic, url_prefix='/elastic')
app.register_blueprint(bp_leads, url_prefix='/leads')
app.register_blueprint(bp_pars, url_prefix='/parser_art')
app.register_blueprint(bp_admin, url_prefix='/admin')
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pars_data.db'
login = LoginManager(app)

login.login_view = '/login'
db = SQLAlchemy(app)


bootstrap = Bootstrap(app)
