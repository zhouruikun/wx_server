#xgc.wechat.py
# app_id='wx7a54e2832a3c92e4'
# app_secret='bd679521867b24bd8dbd79c48a98be63'
#测试账号
app_id='wxc4891c2115ab065e'
app_secret='163ba200ba154a6522a0a0f25247d87f'
#基础授权部分
base_get_access_token = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(app_id,app_secret)
get_ticket = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token='
