from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sub/<str:slug>', views.sub, name='sub'),
    path('create/<str:slug>', views.create, name='create'),
    path('delete/<str:slug>', views.delete, name='delete'),
    path('rename/<str:slug>', views.rename, name='rename'),
    path('uuid/<str:slug>', views.uuid, name='uuid'),
]
