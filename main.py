import sqlite3
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from nris import bp_nris
from elastic.el_search import bp_elastic
from leads_id.leads import bp_leads

path_to_base = '/media/i7_nfs/storage/develop/python/FlaskProject/app.sqlite'
conn = sqlite3.connect(path_to_base)
cursor = conn.cursor()

app = Flask(__name__)
app.register_blueprint(bp_nris, url_prefix='/nris')
app.register_blueprint(bp_elastic, url_prefix='/elastic')
app.register_blueprint(bp_leads, url_prefix='/leads')

app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_COOKIE_SECURE'] = False
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('root.html')


app.run(debug=True, port=6565)
