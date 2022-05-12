import requests
import json


class QrManager:
    def __init__(self):
        self.url = "https://api.qrcode-monkey.com/qr/custom"

    def get_data_post(self):
        payload = {
            "data": "https://ya.ru",
            "config": {
                "body": "circle",
            },
            "size": 300,
            "download": False,
            "file": "png"
        }

        response = requests.post(self.url, json=payload)

        return response


qrm = QrManager()
response = qrm.get_data_post()
print('status:', response.status_code)
print('url:', response.url)

with open('../expiliarmus/QR_POST.png', 'wb') as f:
    f.write(response.content)
