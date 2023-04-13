# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from base64 import b64encode, b64decode
from json import loads
import xui


def index(request):
    return HttpResponse('Hey BITCH!<br>What are you looking for ?! :)')


def sub(request, slug):
    try:
        uuid = b64decode(slug.encode()).decode()
        response = ''
        uris = xui.uri(uuid)
        for i in uris:
            response += uris[i] +'\n\n'
        response = b64encode(response.encode()).decode()
        return HttpResponse(response)
    except:
        return JsonResponse({'successful': False})


def create(request, slug):
    try:
        json = b64decode(slug.encode()).decode()
        user = loads(json)
        xui.create(user['user_id'], user['name'], user['uuid'])
        return JsonResponse({'successful': True})
    except:
        return JsonResponse({'successful': False})


def delete(request, slug):
    try:
        json = b64decode(slug.encode()).decode()
        user = loads(json)
        xui.delete(user['uuid'])
        return JsonResponse({'successful': True})
    except:
        return JsonResponse({'successful': False})


def rename(request, slug):
    try:
        json = b64decode(slug.encode()).decode()
        user = loads(json)
        xui.rename(user['uuid'], user['name'])
        return JsonResponse({'successful': True})
    except:
        return JsonResponse({'successful': False})


def uuid(request, slug):
    try:
        json = b64decode(slug.encode()).decode()
        user = loads(json)
        xui.change_uuid(user['user_id'], user['uuid'])
        return JsonResponse({'successful': True})
    except:
        return JsonResponse({'successful': False})
