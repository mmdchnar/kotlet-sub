from django.shortcuts import render
from django.http import HttpResponse
from base64 import b64encode, b64decode
from sqlite3 import connect
from json import loads


X_UI_DB = 'x-ui.db'
PORT = 2053
DOMAIN = 'www.ay-tof-be-sharafet.top'
EDGES = [
    'mci.ay-tof-be-sharafet.top',
    'mtn.ay-tof-be-sharafet.top',
    'zapas.ay-tof-be-sharafet.top',
    ]
URI = 'vless://$UUID$@$DOMAIN$:$PORT$?mode=gun&security=tls&encryption=none&type=grpc&serviceName=&sni=$SNI$#$NAME$'


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


def index(request):
    return HttpResponse('Hello World!')


def sub(request, uuid):
    try:
        uuid = b64decode(uuid.encode()).decode()
    except:
        uuid = None

    if uuid:
        response = ''
        uris = uri(uuid)
        for i in uris:
            response += uris[i] +'\n\n'
        response = b64encode(response.encode()).decode()
    else:
        response = '404'

    return HttpResponse(response)

