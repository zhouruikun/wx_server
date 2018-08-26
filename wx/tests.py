from django.test import TestCase

# Create your tests here.

from wx import wechart_info
from wx.wechat_api import base_authorization, WechatApi

wechat_api = WechatApi()
wechat_api.post_to_control({'dd':1})
# url = wechart_info.defaults.get('api_control') + '?' + 'access_token=' + ''
# print(type(base_authorization.get_access_token()))