"""wx_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include,path

from wx_server.view import token_check


urlpatterns = [
    path('wx/', include('wx.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    # 增加以下一行，以识别静态资源
    url('MP_verify_DshRWAbSGJZKipZG.txt',token_check),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
