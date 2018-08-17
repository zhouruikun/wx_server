from django.urls import path

from . import views

app_name = 'wx'
urlpatterns = [
    path('', views.index, name='index'),
]
