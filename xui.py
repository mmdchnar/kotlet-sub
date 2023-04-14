from sqlite3 import connect
from json import loads, dumps
from uuid import uuid4
from base64 import b64encode
from datetime import datetime, timedelta

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from consts import *

# Change UUID
def change_uuid(user_id: int, uuid: str):
    conn = connect(X_UI_DB)
    json = conn.execute('select settings from inbounds where port=?', (PORT,)).fetchone()[0]
    settings = loads(json)
    for client in settings['clients']:
        if client['email'][:3] == str(user_id):
            client['id'] = uuid
            conn.execute("update inbounds set settings=? where port=?",
                         (dumps(settings, indent=2), PORT))
            conn.commit()
            conn.close()
            break

# Get config URi
def uri(uuid: str):
    conn = connect(X_UI_DB)
    json = conn.execute('select settings from inbounds where port=?', (PORT,)).fetchone()[0]
    settings = loads(json)
    for client in settings['clients']:
        if client['id'] == uuid:
            uris = {}
            for edge in EDGES:
                uri = URI
                uri = uri.replace('$UUID$', client['id'])
                uri = uri.replace('$DOMAIN$', edge)
                uri = uri.replace('$PORT$', str(PORT))
                uri = uri.replace('$SNI$', DOMAIN)
                uri = uri.replace('$NAME$', f"[{client['email'][:3]}] {client['email'][4:]}")
                uris[edge.split('.')[0].title()] = uri
            return uris

# Rename config
def rename(uuid: str, name: str):
    conn = connect(X_UI_DB)
    json = conn.execute('select settings from inbounds where port=?', (PORT,)).fetchone()[0]
    settings = loads(json)
    for client in settings['clients']:
        if client['id'] == uuid:
            user_id = client['email'][:3]
            client['email'] = f'{user_id} {name}'
            conn.execute("update inbounds set settings=? where port=?",
                            (dumps(settings, indent=2), PORT))
            conn.commit()
            conn.close()
            break

# Delete config
def delete(uuid: str):
    conn = connect(X_UI_DB)
    json = conn.execute('select settings from inbounds where port=?', (PORT,)).fetchone()[0]
    settings = loads(json)
    for client in settings['clients']:
        if client['id'] == uuid:
            settings['clients'].remove(client)
            conn.execute("update inbounds set settings=? where port=?",
                            (dumps(settings, indent=2), PORT))
            conn.commit()
            conn.close()
            break

# Create new config
def create(user_id: int, name: str, uuid: str):
    conn = connect(X_UI_DB)
    name = f'{user_id} {name}'
    json = conn.execute('select settings from inbounds where port=?', (PORT,)).fetchone()[0]
    settings = loads(json)
    now = datetime.now()
    now = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        ) - timedelta(hours=3, minutes=30)
    date = int(now.timestamp()) * 1000

    client = {
        'flow': '',
        'email': name,
        'expiryTime': date,
        'id': uuid,
        'limitIp': 1,
        'totalGB': 0,
        }
    settings['clients'].append(client)
    conn.execute("update inbounds set settings=? where port=?",
                    (dumps(settings, indent=2), PORT))
    conn.commit()
    conn.close()
