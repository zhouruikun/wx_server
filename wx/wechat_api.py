# encoding=utf-8
import hashlib
import json
import random
import string

import time
import urllib.parse

import requests
from django.core.cache import cache
import urllib
import logging



from wx import wechart_info

log = logging.getLogger('./django')


class APIError(object):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


def wx_log_error(APIError):
    log.error('wechat api error: [%s], %s' % (APIError.code, APIError.msg))
    print('wechat api error: [%s], %s' % (APIError.code, APIError.msg))

class base_authorization():
    @classmethod
    def get_ticket(cls):
        key = 'ticket'
        try:
            if cache.has_key(key):
                ticket = cache.get(key)
            else:
                access_token, status = cls.get_access_token()
                ticket = requests.get(wechart_info.get_ticket + access_token).json()['ticket']
                cache.set(key, ticket, 110*60)

            return ticket
        except Exception as Argment:
            print(Argment)
            return Argment

    @staticmethod
    def get_access_token():
        key = 'access_token'
        if (cache.has_key(key)):
            return cache.get(key), True
        print(requests.get(wechart_info.base_get_access_token).json())
        access_token = requests.get(wechart_info.base_get_access_token).json()['access_token']
        cache.set(key, access_token, 110*60)
        return access_token, True


class signature():
    def __init__(self, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': base_authorization.get_ticket(),
            'timestamp': self.__create_timestamp(),
            'url': url,

        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string1 = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)]).encode('utf-8')
        self.ret['signature'] = hashlib.sha1(string1).hexdigest()
        self.ret['appId'] = wechart_info.APPID
        return self.ret
    

class WechatBaseApi(object):
    API_PREFIX = u'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self, appid = wechart_info.APPID, appsecret = wechart_info.APPSECRET, api_entry=None):

        self.config = wechart_info
        self.appid = appid
        self.appsecret = appsecret
        self._access_token = None
        self.api_entry = api_entry or self.API_PREFIX

    @property
    def access_token(self):
        if not self._access_token:
            token, err = base_authorization.get_access_token()
            if err:
                self._access_token = token
                return self._access_token
            else:
                return None

        return self._access_token

    # 解析微信返回的json数据，返回相对应的dict
    def _process_response(self, rsp):
        if 200 != rsp.status_code:
            return None, APIError(rsp.status_code, 'http error')
        try:
            content = rsp.json()
        except Exception:
            return None, APIError(9999, 'invalid response')
        if 'errcode' in content and content['errcode'] != 0:
            return None, APIError(content['errcode'], content['errmsg'])

        return content, None

    def _get(self, path, params=None):
        if not params:
            params = {}

        params['access_token'] = self.access_token

        rsp = requests.get(self.api_entry + path, params=params)

        return self._process_response(rsp)

    def _post(self, path, data, type='json'):
        header = {'content-type': 'application/json'}
        if '?' in path:
            url = self.api_entry + path + 'access_token=' + self.access_token
        else:
            url = self.api_entry + path + '?' + 'access_token=' + self.access_token
        if 'json' == type:
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        rsp = requests.post(url, data, headers=header)
        return self._process_response(rsp)

    def post_to_control(self, data, type='json'):
        header = {'content-type': 'application/json'}

        url = wechart_info.defaults.get('api_control') + '?' + 'access_token=' + self.access_token
        if 'json' == type:
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        rsp = requests.post(url, data, headers=header)
        return self._process_response(rsp)

class WechatApi(WechatBaseApi):

    def get_access_token(self, url=None, **kwargs):
        params = {'grant_type': 'client_credential', 'appid': self.appid, 'secret': self.appsecret}

        if kwargs:
            params.update(kwargs)

        rsp = requests.get(url or self.api_entry + 'token', params)

        return self._process_response(rsp)

    # 返回授权url
    def auth_url(self, redirect_uri, scope='snsapi_userinfo', state=None):
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope\
        =%s&state=%s#wechat_redirect' % (self.appid, urllib.parse.quote(redirect_uri), scope, state if state else '')
        return url
    def get_code_url(self,path = None):
        """微信内置浏览器获取网页授权code的url"""
        url = self.config.defaults.get('wechat_browser_code') + (
            '?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s&path=%s#wechat_redirect' %
            (self.config.APPID, urllib.parse.quote(self.config.REDIRECT_URI),
             self.config.SCOPE, self.config.STATE if self.config.STATE else '', path))
        return url

    def get_code_url_pc(self):
        """pc浏览器获取网页授权code的url"""
        url = self.config.defaults.get('pc_QR_code') + (
            '?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' %
            (self.config.APPID, urllib.parse.quote(self.config.REDIRECT_URI), self.config.PC_LOGIN_SCOPE,
             self.config.STATE if self.config.STATE else ''))
        return url

    # 获取网页授权的access_token
    def get_auth_access_token(self, code):
        url = u'https://api.weixin.qq.com/sns/oauth2/access_token'
        params = {
            'appid': self.appid,
            'secret': self.appsecret,
            'code': code,
            'grant_type': 'authorization_code'
        }

        return self._process_response(requests.get(url, params=params))

    # 获取用户信息
    def get_user_info(self, auth_access_token, openid):
        url = u'https://api.weixin.qq.com/sns/userinfo?'
        params = {
            'access_token': auth_access_token,
            'openid': openid,
            'lang': 'zh_CN'
        }

        return self._process_response(requests.get(url, params=params))


