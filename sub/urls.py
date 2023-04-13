from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sub/<slug:slug>', views.sub, name='sub'),
    path('create/<slug:slug>', views.create, name='create'),
    path('delete/<slug:slug>', views.delete, name='delete'),
    path('rename/<slug:slug>', views.rename, name='rename'),
    path('uuid/<slug:slug>', views.uuid, name='uuid'),
]
