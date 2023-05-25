import os
import requests
from json import loads
from flask import Flask, render_template
from datetime import datetime
from dotenv import load_dotenv
from base64 import b64encode, b64decode
from urllib import parse

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

HOST = os.environ.get("HOST")
PANEL_URL = os.environ.get("PANEL_URL")
API_PATH = os.environ.get("API_PATH")

DOMAINS_keys = os.environ.get("DOMAINS_keys")
DOMAINS_values = os.environ.get("DOMAINS_values")
DOMAINS = dict(zip(DOMAINS_keys.split(','), DOMAINS_values.split(',')))

CONTACT_NAME = os.environ.get("CONTACT_NAME")
CONTACT_LINK = os.environ.get("CONTACT_LINK")

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
print('Logged In!')


def sub(base64_uuid):
    uuid = b64decode(base64_uuid.encode()).decode()
    req = session.get(f'{PANEL_URL}{API_PATH}/get/{INBOUND_ID}')
    clients = loads(req.json()['obj']['settings'])['clients']
    for client in clients:
        if client['id'] == uuid:
            user = session.get(f"{PANEL_URL}{API_PATH}/getClientTraffics/{client['email']}").json()['obj']
            enable = client['enable'] and user['enable']
            usage = round((user['up'] + user['down']) / 1073741824, 2)
            if user['total']:
                total_gb = round(user['total'] / 1073741824, 2)
                gb = (user['total'] - usage)
            else:
                total_gb = 0
                gb = None
            if user['expiryTime']:
                days = (datetime.fromtimestamp(user['expiryTime'] // 1000) - datetime.now()).days
            else:
                days = None
            uris = {}
            for domain in DOMAINS:
                uri = URI
                uri = uri.replace('$UUID$', uuid)
                uri = uri.replace('$DOMAIN$', DOMAINS[domain])
                name = f"{'🟢' if enable else '🔴'} ({domain}) {gb if gb else '∞'} GB | " \
                       f"{days if days else '∞'} Days | {client['email']}"
                name = parse.quote(name)
                uri = uri.replace('$NAME$', name)
                uris[domain] = uri

            configs = ''
            for i in uris:
                configs += uris[i] + '\n\n'
            configs = b64encode(configs.encode()).decode()
            links = {
                'Subscription Link': f'{HOST}/sub/{base64_uuid}',
                'All Links': configs,
            }
            links.update(uris)
            return render_template(
                'user_info.html',
                enable=enable,
                links=links,
                name=user['email'],
                gb=gb,
                total_gb=total_gb,
                usage=usage,
                days=days,
                uris=uris,
                contact_name=CONTACT_NAME,
                contact_link=CONTACT_LINK,
            )


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
    app.run(debug=bool(DEBUG))
