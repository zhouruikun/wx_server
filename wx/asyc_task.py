#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from celery import task
from .wechat_api import WechatBaseApi
import paho.mqtt.publish as publish

@task
def run_api_control(wx_data):
    Wechat = WechatBaseApi()

    wx_data = json.loads(wx_data)
    if '_resp' in wx_data["msg_type"]:
        return True
    res = {
        "asy_error_code": 0,
        "asy_error_msg": "ok",
        "device_id": wx_data["device_id"],
        "device_type": wx_data["device_type"],
        "msg_id": wx_data["msg_id"],
        "user": wx_data["user"],
        "msg_type": wx_data["msg_type"],
        "services": {
            "operation_status":
                {
                 "status": wx_data["services"]["operation_status"]["status"]
                }
         }
    }
    mqtt_send(wx_data["device_id"]+"/sub","led = "+str(1-wx_data["services"]["operation_status"]["status"]))
    result, err = Wechat.post_to_control(data=res)
    if result:
        return True
    else:
        return False
def mqtt_send(topic,data):
    HOST = "106.14.226.150"
    PORT = 1883
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    publish.single(topic, data, qos = 1,hostname=HOST,port=PORT, client_id=client_id)
@task
def run_test_suit(ts_id):
    print("++++++++++++++++++++++++++++++++++++")
    print('jobs[ts_id=%s] running....' % ts_id)
    time.sleep(10.0)
    print('jobs[ts_id=%s] done' % ts_id)
    result = True
    return result