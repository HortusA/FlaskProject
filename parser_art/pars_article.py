import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import re
import sqlite3
from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from bs4 import BeautifulSoup
import pprint
import urllib.parse
import requests


bp_pars = Blueprint('pars_article', __name__, template_folder='templates')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pars_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ParsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pars_string = db.Column(db.String)


class ParserForm(FlaskForm):
    submit = SubmitField("Загрузка базы")


@bp_pars.route('/pars_article', methods=['GET', "POST"])
def pars_content():
    form = ParserForm()
    if form.validate_on_submit():
        a = SearchArticles('app.db')
        result = a.get_article_content()
        test = a.parse_content(date=result[0], content=result[1])
        #for string_pars in test['blocks']:
            #u = ParsTable(pars_string=str(string_pars))
            #db.session.add(u)
            #db.session.flush()
            #db.session.commit()
        #a.write_file("norm.html", a.protocol)
        #a.write_file('errors_url.html', a.url_error)
        a = test
        #print(json.dumps(test))
        return render_template('pars_article/pars_article.html', form=form)
    return render_template('pars_article/pars_article.html', form=form)

def upload_base(data):
    for string_pars in data:
        print(data)





class SearchArticles:
    def __init__(self, path_to_base):
        self.conn = sqlite3.connect(path_to_base)
        self.cursor = self.conn.cursor()
        self.article_body = {}
        self.list_body = []
        self.count = 0
        self.result = None
        self.protocol = []
        self.jpg_list = []
        self.url_error = []

    def execute_one(self, article_id):
        self.cursor.execute("SELECT content FROM cms_article_content WHERE article_id = ?", (article_id,))
        self.result = self.cursor.fetchone()
        return self.result

    def get_article_all(self):
        self.cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                                LEFT JOIN cms_articles a on a.article_id = ac.article_id
                                WHERE a.article_id""")
        return self.cursor.fetchall()

    def list_img(self):
        pass

    def execute_all(self):
        self.cursor.execute("SELECT content FROM cms_article_content")
        self.result = self.cursor.fetchall()
        return self.result

    def get_article_content(self):
        self.cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                                LEFT JOIN cms_articles a on a.article_id = ac.article_id
                                WHERE a.article_id = 7""")
        return self.cursor.fetchone()

    def checking_picture(self, url):
        r = requests.get(url, stream=True)
        for chunk in r.iter_content(chunk_size=256):
            if chunk:
                self.protocol.append(url)
                return 'есть'
            else:
                self.url_error.append(url)
                return 'Нет'

    def check_url(self, i):
        if i.contents and 'src' in i.contents[0].attrs:
            url = (str(i.contents[0].attrs['src']))
            clear_url = urllib.parse.urlsplit(url)
            if clear_url.netloc == "onlinepatent.ru":
                return 'есть'
            else:
                return 'нет'

    def write_file(self, name_files, name_report):
        with open(name_files, 'w') as File:
            File.write('<html>')
            File.write('<body>')
            File.write('<table>')

            for i in name_report:
                File.write(f'<p> {i} </p>')

            File.write('</table>')
            File.write('</body>')
            File.write('</html>')

    def parse_content(self, date, content):
        for content in self.get_article_all():
            clr = re.sub(r"[\\\r\\\n]", "", str(content[1]))
            data_string = BeautifulSoup(clr, 'lxml')

            for i in data_string.body:
                if i.name == 'p':
                    self.list_body.append({
                        "type": "paragraph",
                        "data": {
                            "text": str(i.text),
                        }
                    })
                elif i.name == 'figure':

                    if self.check_url(i) == 'есть':
                        if self.checking_picture(url=str(i.contents[0].attrs['src'])) == 'есть':
                            self.list_body.append(
                                {
                                    "type": "image",
                                    "data": {
                                        "file": {

                                            "url": str(i.contents[0].attrs)
                                        },
                                        "caption": "need to be correct parse",
                                        "withBorder": "false",
                                        "withBackground": "false",
                                        "stretched": "true"
                                    }
                                }
                            )

                elif i.name == 'h2':
                    self.list_body.append(
                        {
                            "type": "header",
                            "data": {
                                "text": str(i.text),
                                "level": 2
                            }
                        }
                    )

        self.article_body.update(
                {
                    "time": date,
                    "blocks": self.list_body,
                    "version": "0.01"
                }
            )

        pprint.pprint(self.url_error)
        return self.article_body


