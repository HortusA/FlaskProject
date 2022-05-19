import re
from bs4 import BeautifulSoup
import pprint
import urllib.parse
import requests
import sqlite3
from bs4.element import Tag


path_to_base = '/home/alex/Документы/amocrm/app.db'
conn = sqlite3.connect(path_to_base)
cursor = conn.cursor()
list_root = []
dict_root = {}


def get_article_all():
    cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                            LEFT JOIN cms_articles a on a.article_id = ac.article_id
                            WHERE a.article_id""")
    return cursor.fetchall()


def check_children(teg):
    list_chlildren = []
    for j in teg.children:


        if j.name == "a" and j.name is not None:
            if 'href' in j.attrs:

                list_chlildren.append(
                    {
                        "type": "url transition",
                        "data": {
                            "file": {

                                "url": str(j.attrs['href'])
                            },
                            "caption": j.text,
                            "withBorder": "false",
                            "withBackground": "false",
                            "stretched": "true"
                        }
                    }
                )

        elif j.name == "strong" and j.name is not None:

            list_chlildren.append({
                "---type": "strong",
                "data": {
                    "text": str(j.text),
                }
            })

        elif j.name == "img" and j.name is not None:
            if 'src' in j.attrs:
                list_chlildren.append(
                    {
                        "type": "image",
                        "data": {
                            "file": {

                                "url": str(j.attrs['src'])
                            },
                            "caption": j.text,
                            "withBorder": "false",
                            "withBackground": "false",
                            "stretched": "true"
                        }
                    }
                )


        elif j.name == "ul" and j.name is not None:
            list_chlildren.append({
                "type": "list ul",
                "data": {
                    "text": str(teg.text),
                }
            })


        elif j.name == "li" and j.name is not None:
            list_chlildren.append({
                "type": "list",
                "data": {
                    "text": str(teg.text),
                }
            })


        elif j.name == "br" and j.name is not None:
            list_chlildren.append({
                "type": "br",
                "data": {
                    "text": str(j.text),
                }
            })


    return list_chlildren

for content in get_article_all():
    date_article = content[0]
    clr = re.sub(r"[\\\r\\\n]", "", str(content))
    soup = BeautifulSoup(clr, 'lxml')
    root = soup.body
    root_childs = [e.name for e in root.children if e.name is not None]
    #print(root_childs)
    root_descendants = [e.name for e in root.descendants if e.name is not None]
    #print(root_descendants)

    for i in root:

        if i.name == "p" and i.name is not None:
            list_root.append(
                {
                    "paragraf": i.text,
                    "block":  check_children(i),
                    "version": "0.01"
                }
            )


        elif i.name == "figure" and i.name is not None:
            list_root.append(
                {
                    "type": 'imeges',
                    "time": check_children(i),
                    "version": "0.01"
                }
            )

        elif i.name == "ul" and i.name is not None:
            list_root.append(
            {
                "paragraf": "UL",
                "time": check_children(i),
                "blocks": list_root,
                "version": "0.01"
            }
            )
    dict_root.update({
        "time": date_article,
        "blocks": list_root,
        "version": "0.01"
    })

    pprint.pprint(dict_root)


    #print(dict_root)
    #root_childs = [e.name for e in root.children if e.name is not None]
   # root_descendants = [e.name for e in root.descendants if e.name is not None]











