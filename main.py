import sqlite3
from flask import render_template
import os
from pathlib import Path
from app import app


path_to_base = os.path.join(Path(__file__).parents[1], 'database.db')
conn = sqlite3.connect(path_to_base)
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template('/home/alex/PycharmProjects/FlaskProject/templates/root.html')


def get_article_all():
    cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                            LEFT JOIN cms_articles a on a.article_id = ac.article_id
                            WHERE a.article_id""")
    return cursor.fetchall()


app.debug = True
app.run(host='0.0.0.0', port=6565)
