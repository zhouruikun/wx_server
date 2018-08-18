import hashlib
import logging
import random
import string


from django.contrib.admin.utils import unquote
import json

from django.core.cache import cache
from django.views import View

from wx_server import wechart_info

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from pip._vendor import requests


@csrf_exempt
def weixin_main(request):
    if request.method == "GET":
        #接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        #服务器配置中的token
        token = 'zhoukuniyc'
        #把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        list = [token, timestamp, nonce]
        list.sort()
        list = ''.join(list)
        hashcode = hashlib.sha1(list.encode()).hexdigest()
        if hashcode == signature:
          return HttpResponse(echostr)
        else:
          return HttpResponse("field")
    else:
        othercontent = autoreply(request)
        return HttpResponse(othercontent)

#微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
import xml.etree.ElementTree as ET
def autoreply(request):
    try:
        webData = request.body
        xmlData = ET.fromstring(webData)

        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        MsgType = xmlData.find('MsgType').text
        MsgId = xmlData.find('MsgId').text

        toUser = FromUserName
        fromUser = ToUserName

        if msg_type == 'text':
            content = "您好,欢迎来到Python大学习!希望我们可以一起进步!"
            replyMsg = TextMsg(toUser, fromUser, content)
            print ("成功了!!!!!!!!!!!!!!!!!!!")
            print (replyMsg)
            return replyMsg.send()

        elif msg_type == 'image':
            content = "图片已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'voice':
            content = "语音已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'video':
            content = "视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'shortvideo':
            content = "小视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'location':
            content = "位置已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            msg_type == 'link'
            content = "链接已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

    except Exception as Argment:
        return Argment

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

import time
class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)

def airkiss(request):

    context = {'test': 'hello'}
    return render(request, 'wx/airkiss.html', context)


class base_authorization():

    @classmethod
    def get_ticket(cls):
        key = 'ticket'
        try:
            if cache.has_key(key):
                ticket  = cache.get(key)
            else:
                if cache.has_key('access_token'):
                    access_token = cache.get('access_token')
                else:
                    access_token = cls.get_access_token()
                ticket = requests.get(wechart_info.get_ticket+access_token).json()['ticket']
                cache.set(key,ticket,110*60)

            return ticket
        except Exception as Argment:
            print(Argment)
            return Argment

    @staticmethod
    def get_access_token():
        key = 'access_token'
        access_token = requests.get(wechart_info.base_get_access_token).json()['access_token']
        cache.set(key,access_token,110*60)

        return access_token

class signature(View):

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

        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)]).encode('utf-8')
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        self.ret['appId'] = wechart_info.app_id
        return self.ret

class activity(View):

    def get(self, request):
        return render(request, 'wx/activaty.html')

    def post(self,request,*args, **kwargs):
        request_type = request.POST.get('type')
        if not request_type:

            request_body = json.loads(request.body.decode())
            pathname = request_body['url']
            sign = signature(unquote(pathname))
            sign = json.dumps(sign.sign())
            return HttpResponse(sign, content_type="application/json")
        elif request_type == 'image/jpeg':
            pass #传图片的时候会用到