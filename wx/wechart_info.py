#xgc.wechat.py
DEBUG_TEST  = True




# -*- coding: utf-8 -*-
# ----------------------------------------------
# @Time    : 18-3-21 上午11:50
# @Author  : YYJ
# @File    : wechatConfig.py
# @CopyRight: ZDWL
# ----------------------------------------------

"""
微信公众号和商户平台信息配置文件
"""


# ----------------------------------------------微信公众号---------------------------------------------- #
if DEBUG_TEST == False:
    APPID = 'wx7a54e2832a3c92e4'
    APPSECRET = 'bd679521867b24bd8dbd79c48a98be63'
else:
    APPID = 'wxc4891c2115ab065e'
    APPSECRET = '163ba200ba154a6522a0a0f25247d87f'



# ----------------------------------------------微信商户平台---------------------------------------------- #
# 商户id
MCH_ID = 'mch_id'

API_KEY = 'api秘钥'


# ----------------------------------------------回调页面---------------------------------------------- #
# 用户授权获取code后的回调页面，如果需要实现验证登录就必须填写
REDIRECT_URI = 'http://wx.zhoukuniyc.top/wx/code'
PC_LOGIN_REDIRECT_URI = 'http://wx.zhoukuniyc.top/wx/code'
#基础授权部分
base_get_access_token = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' %\
                        (APPID, APPSECRET)
get_ticket = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token='

defaults = {
    # 微信内置浏览器获取code微信接口
    'wechat_browser_code': 'https://open.weixin.qq.com/connect/oauth2/authorize',
    # 微信内置浏览器获取access_token微信接口
    'wechat_browser_access_token': 'https://api.weixin.qq.com/sns/oauth2/access_token',
    # 微信内置浏览器获取用户信息微信接口
    'wechat_browser_user_info': 'https://api.weixin.qq.com/sns/userinfo',
    # pc获取登录二维码接口
    'pc_QR_code': 'https://open.weixin.qq.com/connect/qrconnect',
    # pc获取登录二维码接口
    # 'pc_QR_code': 'https://api.weixin.qq.com/sns/userinfo',
    # 微信硬件推送api
    'api_control':'https://api.weixin.qq.com/hardware/mydevice/platform/notify'
}


SCOPE = 'snsapi_userinfo'
PC_LOGIN_SCOPE = 'snsapi_login'
STATE = ''
LANG = 'zh_CN'