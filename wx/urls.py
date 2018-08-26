from django.conf.urls import url

from django.urls import path

from django.views import static
from django.conf import settings

from wx.views import GetUserInfoView, AuthView,AutoFeed
from . import views

app_name = 'wx'
urlpatterns = [
    url(r'^airkiss', views.airkiss.as_view(), name='airkiss'),
    path('main', views.wei_xin_main, name='index'),
    path('api_index', views.wei_api_main, name='api_index'),
    # 授权
    url(r'^auth/$', AuthView.as_view(), name='wx_auth'),
    url(r'^oauth/$', views.oauth.as_view(), name='oauth'),
    # 获取用户信息
    url(r'^code/$', GetUserInfoView.as_view(), name='get_user_info'),
    url(r'^index/$', AuthView.as_view(), name='AuthView'),
    url(r'^api_autofeed/$', AutoFeed.as_view(), name='wx_auth'),
]

