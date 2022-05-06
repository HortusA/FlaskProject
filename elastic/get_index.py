import sqlite3
import os
from elasticsearch import Elasticsearch


es = Elasticsearch('http://192.168.0.111:9200')


path_to_base = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'app.db')
conn = sqlite3.connect(path_to_base)
cursor = conn.cursor()


def execute_all():
    cursor.execute("SELECT article_id, content FROM cms_article_content")
    return cursor.fetchall()


def create_index_es():
    for cont in execute_all():
        es.index(index='my_index', id=cont[0], document={'text': (cont[1])})


create_index_es()
