import logging

import requests
from flask import Flask, request, jsonify

# импортируем функции из нашего второго файла geo

app = Flask(__name__)

# Добавляем логирование в файл.
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return jsonify(response)


@app.route('/')
def index():
    return "Загушка"


def handle_dialog(res, req):
    if 'переведи слово' in req['request']['command'] or \
            'переведите слово' in req['request']['command']:
        word = req['request']['command'].split('слово')[-1].strip()
        res['response']['text'] = translate_(word)
    else:
        res['response']['text'] = 'Для перевода слова введите "Переведите (переведи) слово: *слово*"'


def translate_(word):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    params = {
        'q': word,
        'target': 'en'
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "51dd84cef1msh5ae12c433b80c0dp1b101fjsn3354a2ebb2ac",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=params, headers=headers).json()

    return response['data']['translations'][0]['translatedText']


if __name__ == '__main__':
    app.run()
