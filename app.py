import os
import requests
from json import loads
from flask import Flask
from datetime import datetime
from dotenv import load_dotenv
from base64 import b64encode, b64decode

load_dotenv()

PORT = os.environ.get("PORT")
INBOUND_ID = os.environ.get("INBOUND_ID")
SNI = os.environ.get("SNI")
SID = os.environ.get("SID")
PBK = os.environ.get("PBK")
URI = os.environ.get("URI") \
    .replace('$SNI$', SNI) \
    .replace('$PBK$', PBK) \
    .replace('$SID$', SID) \
    .replace('$PORT$', PORT)
PANEL_URL = os.environ.get("PANEL_URL")
API_PATH = os.environ.get("API_PATH")
DOMAINS_keys = os.environ.get("DOMAINS_keys")
DOMAINS_values = os.environ.get("DOMAINS_values")
DOMAINS = dict(zip(DOMAINS_keys.split(','), DOMAINS_values.split(',')))

USERNAME = os.environ.get("USER")
PASSWORD = os.environ.get("PASS")

DEBUG = int(os.environ.get("DEBUG"))

app = Flask(__name__)

session = requests.session()
session.post(f'{PANEL_URL}/login',
             data={
                 'username': USERNAME,
                 'password': PASSWORD,
             })


def sub(base64_uuid):
    response = 'Kotlet was Eaten by Dogs!! :)'
    uuid = b64decode(base64_uuid.encode()).decode()

    req = session.get(f'{PANEL_URL}{API_PATH}/get/{INBOUND_ID}')
    print('get')
    clients = loads(req.json()['obj']['settings'])['clients']
    for client in clients:
        print(client)
        if client['id'] == uuid:
            user = session.get(f"{PANEL_URL}{API_PATH}/getClientTraffics/{client['email']}").json()['obj']
            print('traffic')
            status = client['enable'] and user['enable']
            status = '🟢' if status else '🔴'
            if user['total']:
                total = (user['total'] - (user['up'] + user['down'])) / 1073741824
                total = round(total, 2)
            else:
                total = '∞'
            if user['expiryTime']:
                expiry = (datetime.fromtimestamp(user['expiryTime'] // 1000) - datetime.now()).days
            else:
                expiry = '∞'
            uris = {}
            for domain in DOMAINS:
                uri = URI
                uri = uri.replace('$UUID$', uuid)
                uri = uri.replace('$DOMAIN$', DOMAINS[domain])
                uri = uri.replace('$NAME$',
                                  f"{status} ({domain}) {total} GB | {expiry} Days | "
                                  f"{client['email'][4:]} {client['email'][:3]}")
                uris[domain] = uri

            response = ''
            for i in uris:
                response += uris[i] + '\n\n'
            response = b64encode(response.encode()).decode()
    return response


@app.route('/sub/<base64_uuid>')
def sub_app(base64_uuid):
    response = 'Kotlet was Eaten by Dogs!! :)'
    if DEBUG:
        response = sub(base64_uuid)
    else:
        try:
            response = sub(base64_uuid)
        except Exception as error:
            print('Error from My Exception: ', error)

    return response


@app.errorhandler(404)
def not_found(e):
    print('from error 404:', e)
    return 'Kotlet was Eaten by Dogs!! :)'


@app.errorhandler(500)
def internal_error(e):
    print('from error 500:', e)
    return 'Kotlet was Eaten by Dogs!! :)'


if __name__ == '__main__':
    app.run()
