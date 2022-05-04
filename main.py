from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
import sqlite3
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, DateField, validators
from werkzeug.utils import secure_filename
from openpyxl import *
from flask_bootstrap import Bootstrap
from os import listdir, path
import shutil
import pathlib
import os
import time

es = Elasticsearch('http://192.168.0.111:9200')
path_to_base = '/home/alex/Документы/amocrm/app.db'  # тестовая база для эластика Задание1 и отчета выборки email из xls фала задание 2
path_to_leads = '/home/alex/Документы/leads'  # путь к каталогу для задачи c папками Задание3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/files'  # куда скчиваться загруженный файл xls пользоваьеля Задача2
app.config['SESSION_COOKIE_SECURE'] = False
bootstrap = Bootstrap(app)

conn = sqlite3.connect(path_to_base)  # подключени к базе для выборик адресов. Задача1 Задание2
cursor = conn.cursor()
list_body = []


class ElasticAddForm(FlaskForm):  # класс для формы элатсика Задание1
    id_doc = IntegerField("id", validators=[DataRequired()])
    elastic_search = TextAreaField("elastic_search", validators=[DataRequired()])
    submit = SubmitField("ок")


class ElasticSearchForm(FlaskForm):
    elastic_search = StringField("elastik_search", validators=[DataRequired()])
    submit = SubmitField("ok")


class NrisForm(FlaskForm):
    submit = SubmitField("ok")


class ElasticSearchIdForm(FlaskForm):
    elastic_search = IntegerField("el_search", validators=[DataRequired()])
    submit = SubmitField("ok")


class ElasticSearchIDForm(FlaskForm):
    elastic_search = IntegerField("el_search", validators=[DataRequired()])
    submit = SubmitField("ok")


class UploadFileForm(FlaskForm):  # Класс формы для загрузки файла задачи Задача1
    file = FileField("file")
    start = DateField("start", format='%Y-%m-%d', validators=(validators.Optional(),))
    end = DateField("end", format='%Y-%m-%d', validators=(validators.Optional(),))
    submit = SubmitField("Загрузка файла")


@app.route('/')  # главная страница проектов
def index():
    return render_template('root.html')


@app.route('/elastic', methods=['GET', "POST"])  # Основной поиск  текста Задание1
def elastic():
    form = ElasticSearchForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        resp = search_text(field_form)
        return render_template('elastic.html', form=form, search_result=resp.body['hits']['hits'])
    return render_template('elastic.html', form=form)


@app.route('/add_id', methods=['GET', "POST"])  # Задание1
def add_id():
    form = ElasticAddForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        id_d = form.id_doc.data
        resp = add_id_es(id_d, field_form)
        return render_template('add_id.html', form=form, search_result=resp)
    return render_template('add_id.html', form=form)


@app.route('/get_id', methods=['GET', "POST"])
def get_id():
    form = ElasticSearchIdForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        try:
            resp = get_id_one(field_form)
        except NotFoundError as ex:
            return f"Документ {field_form} не найден {field_form}{ex}"
        return render_template('search_id.html', form=form, search_result=resp.body['_source']['text'])
    return render_template('search_id.html', form=form)


@app.route('/del_id', methods=['GET', "POST"])
def del_id():
    form = ElasticSearchForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        try:
            resp = del_id_one(field_form)
        except NotFoundError as ex:
            return f"Документ {field_form} не найден {field_form}{ex}"
        return render_template('delete_id.html', form=form, search_result=resp.body['_id'])
    return render_template('delete_id.html', form=form)


@app.route('/upload', methods=['GET', "POST"])  # загрузка файла #Задача2
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        start_data = form.start.data
        end_data = form.end.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                 secure_filename(file.filename))
        file.save(file_path)
        d = EmailList(file_path)
        res = d.list_pyxl(start_data, end_data)

        return render_template('index.html', form=form, data=res)
    return render_template('index.html', form=form)


class EmailList:  # работа с файлом xls для задачи2
    def __init__(self, file_path):
        self.conn = sqlite3.connect(path_to_base)
        self.cursor = self.conn.cursor()
        self.file_path = file_path

    def list_pyxl(self, data_start, data_end):
        self.data_start = data_start
        self.data_end = data_end
        new_xls_email_list = []
        wb = load_workbook(self.file_path)
        for sheet in wb.worksheets:
            if sheet.sheet_state == 'visible':
                column = sheet["A"]
                for one_email in range(len(column)):
                    data_email = str(column[one_email].value)
                    if '@' in data_email:
                        new_xls_email_list.append(data_email)
        print(self.data_end)

        sql = "','".join(new_xls_email_list)
        self.cursor.execute(f"""SELECT
                                    username, sum(amount) as sum
                                    FROM f_lk_payments
                                    WHERE username in ('{sql}')
                                    and time > ('{self.data_start}') and time < ('{self.data_end}')
                                    group by username
                                    """)
        res = self.cursor.fetchall()
        return res


def get_article_all():
    cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                            LEFT JOIN cms_articles a on a.article_id = ac.article_id
                            WHERE a.article_id""")
    return cursor.fetchall()


def execute_all():
    cursor.execute(
        "SELECT article_id, content FROM cms_article_content")  # запрос в базу для выборки всх статей. задача 2
    return cursor.fetchall()


def create_index_es():  # формирование базы для эластика(индексация) задача2
    for cont in execute_all():
        es.index(index='my_index', id=cont[0], document={'text': (cont[1])})


def search_text(text):
    resp = es.search(index="my_index", body={'query': {'match': {'text': text}}})
    print(resp)
    return resp


def add_id_es(id_dic, text):
    resp = es.index(index="my_index", id=id_dic, document={'text': text})
    return resp


def get_id_one(id_d):
    resp = es.get(index="my_index", id=id_d)
    return resp


def del_id_one(id_d):
    resp = es.delete(index="my_index", id=id_d)
    return resp


class CheckingLeads:
    def __init__(self):
        self.path_to_leads = path_to_leads
        self.list_of_duplicate = []
        self.list_separated_leads = []
        self.list_files_in_folder = []
        self.dict_report = {}

    def write_file(self, name_report):  # формирование отчета по папкам задание 3
        name_files = time.strftime("%Y%m%d-%H%M%S") # в качестве имени файла тспользую текущее время
        with open(name_files, 'w') as File:
            for i in name_report:
                File.write(f'{i}')

    @property
    def get_list_leads(self):  # получаю список вех папок в каталоге
        if path.isdir(self.path_to_leads):
            return listdir(self.path_to_leads)
        else:
            print('проверьте путь к каталогу')

    def copy_file(self, dir_def):  # работа с паками  и заполнение словаря для отчета задача 3
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

    def transferring_leads_files(self):  # проверка и создание папки если нет.(приер: 111-222. 111-333. 111-444.
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

