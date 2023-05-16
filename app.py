from flask import Flask
from base64 import b64encode, b64decode
from datetime import datetime
from requests import session
from json import loads
from dotenv import load_dotenv
import os

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

app = Flask(__name__)


@app.route('/')
def index():
    return 'Kotlet was Eaten by Dogs!! :)'


@app.route('/sub/<base64_uuid>')
def sub(base64_uuid):
    response = 'Kotlet was Eaten by Dogs!! :)'

    try:
        uuid = b64decode(base64_uuid.encode()).decode()

        with session() as s:
            s.post(f'{PANEL_URL}/login',
                   data={
                       'username': USERNAME,
                       'password': PASSWORD,
                   })

            req = s.get(f'{PANEL_URL}{API_PATH}/get/{INBOUND_ID}')
            clients = loads(req.json()['obj']['settings'])['clients']
            for client in clients:
                if client['id'] == uuid:
                    user = s.get(f"{PANEL_URL}{API_PATH}/getClientTraffics/{client['email']}").json()['obj']
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
    except Exception as error:
        print('Error from My Exception: ', error)

    return response


if __name__ == '__main__':
    app.run()
