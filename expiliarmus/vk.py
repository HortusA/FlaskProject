import requests

TOKEN = 'aa073b2daa073b2daa073b2d2baa7265a1aaa07aa073b2df5c878474af5fe832c707988'
URL = 'https://api.vk.com/'


def get_vk_url():
    response = requests.get(f"https://api.vk.com/method/utils.getShortLink?url={URL}&private=0&v=5.131&access_token={TOKEN}")
    json_url = response.json()
    url_vk = json_url['response']["short_url"]
    return url_vk



get_vk_url()

