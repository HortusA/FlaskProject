import sqlite3
from flask import render_template
import os
from pathlib import Path
from app import app
from nris import bp_nris
from elastic.el_search import bp_elastic
from leads_id.leads import bp_leads
from parser_art.pars_article import bp_pars
from user_login_panel.login_user import bp_admin
from grossFile import bp_file

app.register_blueprint(bp_nris, url_prefix='/nris')
app.register_blueprint(bp_elastic, url_prefix='/elastic')
app.register_blueprint(bp_leads, url_prefix='/leads')
app.register_blueprint(bp_pars, url_prefix='/parser_art')
app.register_blueprint(bp_admin, url_prefix='/user_login')
app.register_blueprint(bp_file, url_prefix='/gross_file')

path_to_base = os.path.join(Path(__file__).parents[1], 'database.db')
conn = sqlite3.connect(path_to_base)
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template('root.html')


def get_article_all():
    cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                            LEFT JOIN cms_articles a on a.article_id = ac.article_id
                            WHERE a.article_id""")
    return cursor.fetchall()


app.debug = True
app.run(host='0.0.0.0', port=6565)
