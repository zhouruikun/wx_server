from django.conf.urls import url

from django.urls import path

from django.views import static
from django.conf import settings
from . import views

app_name = 'wx'
urlpatterns = [
    path('', views.weixin_main, name='index'),
# 增加以下一行，以识别静态资源
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static')
]
