import hashlib
import urllib
from django.contrib.admin.utils import unquote
import json
from django.urls import reverse
from django.views import View
from wx.models import User
from wx.wechat_api import wx_log_error, signature, WechatApi
from django.http import HttpResponse, HttpResponseServerError, Http404
from django.shortcuts import render, redirect

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
import paho.mqtt.publish as publish
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


def mqtt_send(topic,data):
    HOST = "106.14.226.150"
    PORT = 1883
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    publish.single(topic, data, qos = 1,hostname=HOST,port=PORT, client_id=client_id)

def autoreply(request):
    try:
        webData = request.body

        xmlData = ET.fromstring(webData)
        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        print(webData)
        if xmlData.find('Content') != None:
            Content_recv = xmlData.find('Content').text
        else:
            Content_recv = ''
        toUser = FromUserName
        fromUser = ToUserName

        if msg_type == 'text':
            content = "周坤真帅"
            if "led" in Content_recv:
                mqtt_send('ESP8266/sample/sub',Content_recv)
                replyMsg = TextMsg(toUser, fromUser, "操作成功 你真厉害")
            else:
                replyMsg = TextMsg(toUser, fromUser, content)
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
        elif msg_type == 'link':
            content = "链接已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'event':

            EventKey = xmlData.find('EventKey').text
            if EventKey == 'key_light_on':
                mqtt_send('ESP8266/sample/sub', 'led = 1')
                content = "已经开灯，周坤真帅"
            else:
                mqtt_send('ESP8266/sample/sub',  'led = 0')
                content = "已经关灯，周坤真帅"

            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            content = "发的啥玩意"
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



class airkiss(View):

    def get(self, request):
        return render(request, 'wx/airkiss.html')

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


class AuthView(View):

    def dispatch(self, request, *args, **kwargs):
        # 判断是否有授权
        if not 'user' in request.session:
            # 用户需要访问的url路径
            path = request.get_full_path()

            # 跳转url,
            red_url = '%s?path=%s' % (reverse('wx_auth'), urllib.quote(path))
            return redirect(red_url)

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class GetUserInfoView(View):#
    def get(self, request):

        redir_url = request.GET.get('path')
        code = request.GET.get('code')

        if redir_url and code:

            # 获取网页授权access_token
            token_data, error = WechatApi.get_auth_access_token(code)

            if error:
                wx_log_error(error)
                return HttpResponseServerError('get access_token error')

            # 获取用户信息信息
            user_info, error =  WechatApi.get_user_info(token_data['access_token'], token_data['openid'])

            if error:
                wx_log_error(error)
                return HttpResponseServerError('get userinfo error')

            # 存储用户信息
            user = self._save_user(user_info)
            if not user:
                return HttpResponseServerError('save userinfo error')

            # 用户对象存入session
            request.session['user'] = user

            # 跳转回目标页面
            return redirect(redir_url)

        # 用户禁止授权后怎么操作
        else:
            return Http404('parameter path or code not founded!!')

    def _save_user(self, data):
        user = User.objects.filter(openid=data['openid'])

        # 没有则存储用户数据，有返回用户数据的字典
        if 0 == user.count():
            user_data = {
                'nick': data['nickname'].encode('iso8859-1').decode('utf-8'),
                'openid': data['openid'],
                'avatar': data['headimgurl'],
                'info': self._user2utf8(data),
            }

            if 'unionid' in data:
                user_data.update('unionid', data.unionid)

            try:
                new_user = User(**user_data)
                new_user.save()

                user_data.update({'id': new_user.id})

                return user_data
            except Exception as e:
                print(e)

            return None
        else:
            # 把User对象序列化成字典，具体看rest_framework中得内容
            return ''#UserSerializer(user[0]).data


    # 解决中文显示乱码问题
    def _user2utf8(self, user_dict):
        utf8_user_info = {
            "openid": user_dict['openid'],
            "nickname": user_dict['nickname'].encode('iso8859-1').decode('utf-8'),
            "sex": user_dict['sex'],
            "province": user_dict['province'].encode('iso8859-1').decode('utf-8'),
            "city": user_dict['city'].encode('iso8859-1').decode('utf-8'),
            "country": user_dict['country'].encode('iso8859-1').decode('utf-8'),
            "headimgurl": user_dict['headimgurl'],
            "privilege": user_dict['privilege'],
        }

        if 'unionid' in user_dict:
            utf8_user_info.update({'unionid': user_dict['unionid']})

        return utf8_user_info

