from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
import sqlite3
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, DateField, validators
from openpyxl import *
from flask_bootstrap import Bootstrap
from os import listdir, path
import shutil
import pathlib
import os
import time
from nris import bp_nris
from elastic.el_search import bp_elastic


path_to_base = '/home/alex/Документы/amocrm/app.db'
conn = sqlite3.connect(path_to_base)
cursor = conn.cursor()


path_to_leads = '/home/alex/Документы/leads'


app = Flask(__name__)
app.register_blueprint(bp_nris, url_prefix='/nris')
app.register_blueprint(bp_elastic, url_ptefix = '/elastic')

app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_COOKIE_SECURE'] = False
bootstrap = Bootstrap(app)





@app.route('/') #главная страница проектов
def index():
    return render_template('root.html')





def get_article_all():
    cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                            LEFT JOIN cms_articles a on a.article_id = ac.article_id
                            WHERE a.article_id""")
    return cursor.fetchall()


def create_index_es(): # формирование базы для эластика(индексация) задача2
    for cont in execute_all():
        es.index(index='my_index', id=cont[0], document={'text': (cont[1])})




def nris():
    a = CheckingLeads()
    a.transferring_leads_files()
    a.write_file(a.list_of_duplicate)
    return 'ок'


class CheckingLeads:
    def __init__(self):
        self.path_to_leads = path_to_leads
        self.list_of_duplicate = []
        self.list_separated_leads = []
        self.list_files_in_folder = []
        self.dict_report = {}

    def write_file(self, name_report): # формирование отчета по папкам задание 3
        name_files = time.strftime("%Y%m%d-%H%M%S")
        with open(name_files, 'w') as File:

            for i in name_report:
                File.write(f'{i}')

    @property
    def get_list_leads(self):
        if path.isdir(self.path_to_leads):
            return listdir(self.path_to_leads)
        else:
            print('проверьте путь к каталогу')

    def copy_file(self, dir_def):# работа с паками  и заполнение словаря для отчета задача 3
        get_files = listdir(pathlib.Path(path_to_leads, '-'.join(dir_def)))
        for file in get_files:
            path_from_ware = (pathlib.Path(path_to_leads, '-'.join(dir_def), file))
            path_ware = (pathlib.Path(path_to_leads, dir_def[0], file))
            if not path.exists(path_ware):
                if path.isfile(pathlib.Path(path_to_leads, path_from_ware)):
                    shutil.copy(path_from_ware, path_ware)
                else:
                    shutil.copytree(path_from_ware, path_ware)
                self.list_of_duplicate.append(
                                {
                                    "Исходная директория": path_from_ware,
                                    "Конечная директория": {
                                        "Путь": path_from_ware,
                                        "файл": file,
                                        "Тип оперции": "Копирование"
                                            }
                                }
                            )

            else:
                self.list_of_duplicate.append(
                                {
                                    "Исходная директория": path_from_ware,
                                    "Конечная директория": {
                                        "Путь": path_from_ware,
                                        "файл": file,
                                        "Тип оперции": "Ошибка. Файл в каталоге присутствует"
                                            }
                                }
                            )
        self.dict_report.update(self.list_of_duplicate)

    def transferring_leads_files(self): # проверка и создание папки если нет. 111-222. 111-333. 111-444.
        for dir_in_leads in self.get_list_leads:  # должна быть папка 111, если нет то то создаем и переосим все туда Задание3
            if path.isdir(pathlib.Path(path_to_leads, dir_in_leads)) and \
                    len(os.listdir(pathlib.Path(path_to_leads, dir_in_leads))) != 0:
                if '-' in dir_in_leads:
                    dir_def = (dir_in_leads.split('-'))
                    if dir_def[0] in self.get_list_leads:
                        self.copy_file(dir_def)
                    else:
                        if dir_def[0] not in self.get_list_leads:
                            os.makedirs(pathlib.Path(path_to_leads, dir_def[0]))
                            self.list_of_duplicate.append(
                                {
                                    "Исходная директория": path_to_leads,
                                    "Конечная директория": {
                                        "Путь": pathlib.Path(path_to_leads, dir_def[0]),
                                        "Директория": dir_def[0],
                                        "Тип оперции": "Директория отсутствовала и быда создана"
                                    }
                                }
                            )
                            self.copy_file(dir_def)


app.run(debug=True)

