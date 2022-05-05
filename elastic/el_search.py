from flask import render_template, Blueprint
from elasticsearch import Elasticsearch
from wtforms.validators import DataRequired
from elasticsearch.exceptions import NotFoundError
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, StringField, SubmitField


es = Elasticsearch('http://192.168.0.111:9200')
bp_elastic = Blueprint('elastic', __name__)


class ElasticAddForm(FlaskForm):
    id_doc = IntegerField("id", validators=[DataRequired()])
    elastic_search = TextAreaField("elastic_search", validators=[DataRequired()])
    submit = SubmitField("ок")


class ElasticSearchForm(FlaskForm):
    elastic_search = StringField("elastik_search", validators=[DataRequired()])
    submit = SubmitField("ok")


class ElasticSearchIdForm(FlaskForm):
    elastic_search = IntegerField("elastik_search", validators=[DataRequired()])
    submit = SubmitField("ok")


class ElasticSearchIDForm(FlaskForm):
    elastic_search = IntegerField("elastik_search", validators=[DataRequired()])
    submit = SubmitField("ok")


@bp_elastic.route('/elastic', methods=['GET', "POST"]) #Основной поиск  текста Задание1
def elastic():
    form = ElasticSearchForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        resp = search_text(field_form)
        return render_template('elastic/elastic.html', form=form, search_result=resp.body['hits']['hits'])
    return render_template('elastic/elastic.html', form=form)


@bp_elastic.route('/add_id', methods=['GET', "POST"]) #Задание1
def add_id():
    form = ElasticAddForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        id_d = form.id_doc.data
        resp = add_id_es(id_d, field_form)
        return render_template('elastic/add_id.html', form=form, search_result=resp)
    return render_template('elastic/add_id.html', form=form)


@bp_elastic.route('/get_id', methods=['GET', "POST"])
def get_id():
    form = ElasticSearchIdForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        try:
            resp = get_id_one(field_form)
        except NotFoundError as ex:
            return f"Документ {field_form} не найден {field_form}{ex}"
        return render_template('elastic/search_id.html', form=form, search_result=resp.body['_source']['text'])
    return render_template('elastic/search_id.html', form=form)


@bp_elastic.route('/del_id', methods=['GET', "POST"])
def del_id():
    form = ElasticSearchForm()
    if form.validate_on_submit():
        field_form = form.elastic_search.data
        try:
            resp = del_id_one(field_form)
        except NotFoundError as ex:
            return f"Документ {field_form} не найден {field_form}{ex}"
        return render_template('elastic/delete_id.html', form=form, search_result=resp.body['_id'])
    return render_template('elastic/delete_id.html', form=form)


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


def create_index_es():
    for cont in execute_all():
        es.index(index='my_index', id=cont[0], document={'text': (cont[1])})