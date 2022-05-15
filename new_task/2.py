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




def get_article_all():
    cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                            LEFT JOIN cms_articles a on a.article_id = ac.article_id
                            WHERE a.article_id""")
    return cursor.fetchall()




for content in get_article_all():
    article_body = {}
    date_article = content[0]
    clr = re.sub(r"[\\\r\\\n]", "", str(content))
    soup = BeautifulSoup(clr, 'lxml')
    root = soup.body
    root_root = [e.name for e in root if e.name is not None]
    #print(root_root)
    root_childs = [e.name for e in root.children if e.name is not None]
    #print(root_childs)
    root_descendants = [e.name for e in root.descendants if e.name is not None]
    #print(root_descendants)
    list_root = []
    for i in root:
        if i.name is not None:
            list_in=[]
            for teg in i.descendants:
                if teg.name is not None:
                    if teg.name == 'strong':

                        list_in.append({"type": "strong","data": {"text": str(i.text)
                            }
                        }
                    )

                    elif teg.name == "img" and teg.name is not None:
                        if 'src' in teg.attrs:
                            list_in.append(
                                {
                                    "type": "image",
                                    "data": {
                                        "file": {

                                            "url": str(teg.attrs['src'])
                                        },
                                        "caption": teg.text,
                                        "withBorder": "false",
                                        "withBackground": "false",
                                        "stretched": "true"
                                    }
                                }
                            )
                    elif teg.name == "li" and teg.name is not None:
                        list_in.append({
                            "type": "li",
                            "data": {
                                "text": str(teg.text),
                            }
                        })
                    elif teg.name == "a" and teg.name is not None:
                        if 'href' in teg.attrs:
                            list_in.append(
                                {
                                    "type": "url transition",
                                    "data": {
                                        "file": {

                                            "url": str(teg.attrs['href'])
                                        },
                                        "caption": teg.text,
                                        "withBorder": "false",
                                        "withBackground": "false",
                                        "stretched": "true"
                                    }
                                }
                            )
                    elif teg.name == 'em' and teg.name is not None:
                        list_in.append({
                            "type": 'em',
                            "data": {
                                "text": str(teg),
                            }
                        })

                    elif teg.name == 'table' and teg.name is not None:
                        list_in.append({
                            "type": 'em',
                            "data": {
                                "text": str(teg),
                            }
                        })
                    elif teg.name == 'tbody' and teg.name is not None:
                        list_in.append({
                            "type": 'tbody',
                            "data": {
                                "text": str(teg),
                            }
                        })


            list_root.append({
                   "data": {'Name teg':i.name,'тег': teg.text,
                    "text": list_in,
                }
            })

            article_body.update({'dtatdict': list_root})
    #print(list_root)




    print(article_body)