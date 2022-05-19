import requests

TOKEN = 'aa073b2daa073b2daa073b2d2baa7265a1aaa07aa073b2df5c878474af5fe832c707988'
URL = 'https://api.vk.com/'
t="c0b769e6911c7f007834db475db265767f67bed55b2a1758511b69e88df343c0d43204dc1512c5eb59c58"


def get_vk_url():
    response = requests.get(f"https://api.vk.com/method/utils.getShortLink?url={URL}&private=0&v=5.131&access_token={TOKEN}")
    json_url = response.json()
    url_vk = json_url['response']["short_url"]
    return url_vk

def getsrvicekey():
    response = requests.get(f"https://api.vk.com/method/utils.getShortLink?url={URL}&private=0&v=5.131&access_token={t}")

    res = requests.get(f'https://oauth.vk.com/authorize?client_id=8164687&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.131')
    print(response.text)

getsrvicekey()