from django.conf.urls import url

from django.urls import path

from django.views import static
from django.conf import settings

from wx.views import GetUserInfoView, AuthView
from . import views

app_name = 'wx'
urlpatterns = [
    url(r'^airkiss', views.airkiss.as_view(), name='airkiss'),
    path('main', views.weixin_main, name='index'),
    # 授权
    url(r'^auth/$', AuthView.as_view(), name='wx_auth'),
    # 获取用户信息
    url(r'^code/$', GetUserInfoView.as_view(), name='get_user_info'),
    url(r'^index/$', GetUserInfoView.as_view(), name='get_user_info'),

]

