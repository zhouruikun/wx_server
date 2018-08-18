from django.conf.urls import url

from django.urls import path

from django.views import static
from django.conf import settings
from . import views

app_name = 'wx'
urlpatterns = [
    url(r'^activity', views.activity.as_view(), name='activity'),
    path('main', views.weixin_main, name='index'),
    path('airkiss', views.airkiss, name='airkiss'),

]
