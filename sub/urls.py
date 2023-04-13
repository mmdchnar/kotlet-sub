from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sub/<slug:uuid>', views.sub, name='sub'),
]
