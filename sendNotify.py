# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/28

import sys
import os, re
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse

# 通知服务
BARK = ''                   # bark服务,自行搜索; secrets可填;
SCKEY = ''                  # Server酱的SCKEY; secrets可填
TG_BOT_TOKEN = ''           # tg机器人的TG_BOT_TOKEN; secrets可填1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ
TG_USER_ID = ''             # tg机器人的TG_USER_ID; secrets可填 1434078534
TG_API_HOST=''              # tg 代理api
TG_PROXY_HOST = ''          # tg机器人的TG_PROXY_HOST; secrets可填
TG_PROXY_PORT = ''          # tg机器人的TG_PROXY_PORT; secrets可填
DD_BOT_TOKEN = ''           # 钉钉机器人的DD_BOT_TOKEN; secrets可填
DD_BOT_SECRET = ''          # 钉钉机器人的DD_BOT_SECRET; secrets可填
QQ_SKEY = ''                # qq机器人的QQ_SKEY; secrets可填
QQ_MODE = ''                # qq机器人的QQ_MODE; secrets可填
QYWX_AM = ''                # 企业微信
PUSH_PLUS_TOKEN = ''        # 微信推送Plus+
PUSH_PLUS_USER= ''          # plus+群组编码,可为空

notify_mode = []
message_info = ''''''

# GitHub action运行需要填写对应的secrets
if "BARK" in os.environ and os.environ["BARK"]:
    BARK = os.environ["BARK"]
if "SCKEY" in os.environ and os.environ["SCKEY"]:
    SCKEY = os.environ["SCKEY"]
if "TG_BOT_TOKEN" in os.environ and os.environ["TG_BOT_TOKEN"] and "TG_USER_ID" in os.environ and os.environ["TG_USER_ID"]:
    TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
    TG_USER_ID = os.environ["TG_USER_ID"]
if "TG_API_HOST" in os.environ and os.environ["TG_API_HOST"]:
    TG_API_HOST = os.environ["TG_API_HOST"]
if "DD_BOT_TOKEN" in os.environ and os.environ["DD_BOT_TOKEN"] and "DD_BOT_SECRET" in os.environ and os.environ["DD_BOT_SECRET"]:
    DD_BOT_TOKEN = os.environ["DD_BOT_TOKEN"]
    DD_BOT_SECRET = os.environ["DD_BOT_SECRET"]
if "QQ_SKEY" in os.environ and os.environ["QQ_SKEY"] and "QQ_MODE" in os.environ and os.environ["QQ_MODE"]:
    QQ_SKEY = os.environ["QQ_SKEY"]
    QQ_MODE = os.environ["QQ_MODE"]
# 获取pushplus+ PUSH_PLUS_TOKEN
if "PUSH_PLUS_TOKEN" in os.environ:
    if len(os.environ["PUSH_PLUS_TOKEN"]) > 1:
        PUSH_PLUS_TOKEN = os.environ["PUSH_PLUS_TOKEN"]
        # print("已获取并使用Env环境 PUSH_PLUS_TOKEN")
if "PUSH_PLUS_USER" in os.environ:
    if len(os.environ["PUSH_PLUS_USER"]) > 0:
        PUSH_PLUS_USER = os.environ["PUSH_PLUS_USER"]
        # print("已获取并使用Env环境 PUSH_PLUS_USER")

# 获取企业微信应用推送 QYWX_AM
if "QYWX_AM" in os.environ:
    if len(os.environ["QYWX_AM"]) > 1:
        QYWX_AM = os.environ["QYWX_AM"]
        # print("已获取并使用Env环境 QYWX_AM")

if BARK:
    notify_mode.append('bark')
    # print("BARK 推送打开")
if SCKEY:
    notify_mode.append('sc_key')
    # print("Server酱 推送打开")
if TG_BOT_TOKEN and TG_USER_ID:
    notify_mode.append('telegram_bot')
    # print("Telegram 推送打开")
if DD_BOT_TOKEN and DD_BOT_SECRET:
    notify_mode.append('dingding_bot')
    # print("钉钉机器人 推送打开")
if QQ_SKEY and QQ_MODE:
    notify_mode.append('coolpush_bot')
    # print("QQ机器人 推送打开")

if PUSH_PLUS_TOKEN:
    notify_mode.append('pushplus_bot')
    # print("微信推送Plus机器人 推送打开")
if QYWX_AM:
    notify_mode.append('wecom_app')
    # print("企业微信机器人 推送打开")

def initialize(d):
    # 通知服务
    global notify_mode,message_info,BARK,SCKEY,TG_BOT_TOKEN,TG_USER_ID,TG_API_HOST,TG_PROXY_HOST,TG_PROXY_PORT,DD_BOT_TOKEN,DD_BOT_SECRET,Q_SKEY,QQ_MODE,QYWX_AM,PUSH_PLUS_TOKEN,PUSH_PLUS_USER
    message_info = ''''''
    notify_mode = []
    try:
        BARK=d['BARK']                          # bark服务,自行搜索; secrets可填;
    except:
        BARK=''
    try:
        SCKEY=d['SCKEY']                        # Server酱的SCKEY; secrets可填
    except:
        SCKEY=''
    try:
        TG_BOT_TOKEN=d['TG_BOT_TOKEN']          # tg机器人的TG_BOT_TOKEN; secrets可填1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ
    except:
        TG_BOT_TOKEN=''
    try:
        TG_USER_ID=d['TG_USER_ID']              # tg机器人的TG_USER_ID; secrets可填 1434078534
    except:
        TG_USER_ID=''
    try:
        TG_API_HOST=d['TG_API_HOST']            # tg 代理api
    except:
        TG_API_HOST=''
    try:
        TG_PROXY_HOST=d['TG_PROXY_HOST']        # tg机器人的TG_PROXY_HOST; secrets可填
    except:
        TG_PROXY_HOST=''
    try:
        TG_PROXY_PORT=d['TG_PROXY_PORT']        # tg机器人的TG_PROXY_PORT; secrets可填
    except:
        TG_PROXY_PORT=''
    try:
        DD_BOT_TOKEN=d['DD_BOT_TOKEN']          # 钉钉机器人的DD_BOT_TOKEN; secrets可填
    except:
        DD_BOT_TOKEN=''
    try:
        DD_BOT_SECRET=d['DD_BOT_SECRET']        # 钉钉机器人的DD_BOT_SECRET; secrets可填
    except:
        DD_BOT_SECRET=''
    try:
        QQ_SKEY=d['QQ_SKEY']                    # qq机器人的QQ_SKEY; secrets可填
    except:
        QQ_SKEY=''
    try:
        QQ_MODE=d['QQ_MODE']                    # qq机器人的QQ_MODE; secrets可填
    except:
        QQ_MODE=''
    try:
        QYWX_AM=d['QYWX_AM']                    # 企业微信
    except:
        QYWX_AM=''
    try:
        PUSH_PLUS_TOKEN=d['PUSH_PLUS_TOKEN']    # 微信推送Plus+
    except:
        PUSH_PLUS_TOKEN=''
    try:
        PUSH_PLUS_USER=d['PUSH_PLUS_USER']      # plus+群组编码,可为空
    except:
        PUSH_PLUS_USER=''

    notify_mode = []
    message_info = ''''''

    # GitHub action运行需要填写对应的secrets
    if "BARK" in os.environ and os.environ["BARK"]:
        BARK = os.environ["BARK"]
    if "SCKEY" in os.environ and os.environ["SCKEY"]:
        SCKEY = os.environ["SCKEY"]
    if "TG_BOT_TOKEN" in os.environ and os.environ["TG_BOT_TOKEN"] and "TG_USER_ID" in os.environ and os.environ["TG_USER_ID"]:
        TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
        TG_USER_ID = os.environ["TG_USER_ID"]
    if "TG_API_HOST" in os.environ and os.environ["TG_API_HOST"]:
        TG_API_HOST = os.environ["TG_API_HOST"]
    if "DD_BOT_TOKEN" in os.environ and os.environ["DD_BOT_TOKEN"] and "DD_BOT_SECRET" in os.environ and os.environ["DD_BOT_SECRET"]:
        DD_BOT_TOKEN = os.environ["DD_BOT_TOKEN"]
        DD_BOT_SECRET = os.environ["DD_BOT_SECRET"]
    if "QQ_SKEY" in os.environ and os.environ["QQ_SKEY"] and "QQ_MODE" in os.environ and os.environ["QQ_MODE"]:
        QQ_SKEY = os.environ["QQ_SKEY"]
        QQ_MODE = os.environ["QQ_MODE"]
    # 获取pushplus+ PUSH_PLUS_TOKEN
    if "PUSH_PLUS_TOKEN" in os.environ:
        if len(os.environ["PUSH_PLUS_TOKEN"]) > 1:
            PUSH_PLUS_TOKEN = os.environ["PUSH_PLUS_TOKEN"]
            # print("已获取并使用Env环境 PUSH_PLUS_TOKEN")
    if "PUSH_PLUS_USER" in os.environ:
        if len(os.environ["PUSH_PLUS_USER"]) > 0:
            PUSH_PLUS_USER = os.environ["PUSH_PLUS_USER"]
            # print("已获取并使用Env环境 PUSH_PLUS_USER")

    # 获取企业微信应用推送 QYWX_AM
    if "QYWX_AM" in os.environ:
        if len(os.environ["QYWX_AM"]) > 1:
            QYWX_AM = os.environ["QYWX_AM"]
            # print("已获取并使用Env环境 QYWX_AM")

    if BARK:
        notify_mode.append('bark')
        # print("BARK 推送打开")
    if SCKEY:
        notify_mode.append('sc_key')
        # print("Server酱 推送打开")
    if TG_BOT_TOKEN and TG_USER_ID:
        notify_mode.append('telegram_bot')
        # print("Telegram 推送打开")
    if DD_BOT_TOKEN and DD_BOT_SECRET:
        notify_mode.append('dingding_bot')
        # print("钉钉机器人 推送打开")
    if QQ_SKEY and QQ_MODE:
        notify_mode.append('coolpush_bot')
        # print("QQ机器人 推送打开")

    if PUSH_PLUS_TOKEN:
        notify_mode.append('pushplus_bot')
        # print("微信推送Plus机器人 推送打开")
    if QYWX_AM:
        notify_mode.append('wecom_app')
        # print("企业微信机器人 推送打开")


def msg(*args):
    global message_info
    a=''
    for str_msg in args:
        a=a+' '+str(str_msg)
    a=a[1:]
    print(a)
    message_info = f"{message_info}\n{a}"
    sys.stdout.flush()

def bark(title, content):
    print("\n")
    if not BARK:
        print("bark服务的bark_token未设置!!\n取消推送")
        return
    print("bark服务启动")
    try:
        response = requests.get(
            f"""https://api.day.app/{BARK}/{title}/{urllib.parse.quote_plus(content)}""").json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except:
        print('推送失败！')

def serverJ(title, content):
    print("\n")
    if not SCKEY:
        print("server酱服务的SCKEY未设置!!\n取消推送")
        return
    print("serverJ服务启动")
    data = {
        "text": title,
        "desp": content.replace("\n", "\n\n")
    }
    response = requests.post(f"https://sc.ftqq.com/{SCKEY}.send", data=data).json()
    if response['errno'] == 0:
        print('推送成功！')
    else:
        print('推送失败！')

# tg通知
def telegram_bot(title, content):
 
def dingding_bot(title, content):
   

def coolpush_bot(title, content):
  

# push+推送
def pushplus_bot(title, content):
    global PUSH_PLUS_USER
    try:
        if not PUSH_PLUS_TOKEN:
            print("push+ 服务的token未设置!!\n取消推送")
            return
        data={
            "token": PUSH_PLUS_TOKEN,
            "title": title,
            "content": content,
            "topic": PUSH_PLUS_USER,
        }
        print("push+ 服务启动")
        url='https://www.pushplus.plus/send'
        headers={
            "Content-Type":"application/json"
		}
        data=json.dumps(data).encode(encoding='utf-8')
        response = requests.post(url=url, data=data, headers=headers).json()
        if response['code']==200:
            print(f"push+ 推送成功！")
        else:
            print(f"push+ 推送失败！")
            print(response) 
    except Exception as e:
        print(e)

# 企业微信 APP 推送
def wecom_app(title, content):
    try:
        if not QYWX_AM:
            print("QYWX_AM 并未设置！！\n取消推送")
            return
        QYWX_AM_AY = re.split(',', QYWX_AM)
        if 4 < len(QYWX_AM_AY) > 5:
            print("QYWX_AM 设置错误！！\n取消推送")
            return
        print("企业微信应用服务启动")
        corpid = QYWX_AM_AY[0]
        corpsecret = QYWX_AM_AY[1]
        touser = QYWX_AM_AY[2]
        agentid = QYWX_AM_AY[3]
        try:
            media_id = QYWX_AM_AY[4]
        except:
            media_id = ''
        wx = WeCom(corpid, corpsecret, agentid)
        # 如果没有配置 media_id 默认就以 text 方式发送
        if not media_id:
            message = title + '\n\n' + content
            response = wx.send_text(message, touser)
        else:
            response = wx.send_mpnews(title, content, media_id, touser)
        if response == 'ok':
            print('推送成功！')
        else:
            print('推送失败！错误信息如下：\n', response)
    except Exception as e:
        print(e)



   

def send(title,text=''):
    """
    使用 bark, telegram bot, dingding bot, serverJ 发送手机推送
    :param title:
    :param content:
    :return:
    """
    content=text+'\n'+message_info
    content += '\n\n项目地址By: https://github.com/wuye999/myScripts'
    for i in notify_mode:
        if i == 'bark':
            if BARK:
                bark(title=title, content=content)
            else:
                print('未启用 bark')
            continue
        if i == 'sc_key':
            if SCKEY:
                serverJ(title=title, content=content)
            else:
                print('未启用 Server酱')
            continue
        elif i == 'dingding_bot':
            if DD_BOT_TOKEN and DD_BOT_SECRET:
                dingding_bot(title=title, content=content)
            else:
                print('未启用 钉钉机器人')
            continue
        elif i == 'telegram_bot':
            if TG_BOT_TOKEN and TG_USER_ID:
                telegram_bot(title=title, content=content)
            else:
                print('未启用 telegram机器人')
            continue
        elif i == 'coolpush_bot':
            if QQ_SKEY and QQ_MODE:
                coolpush_bot(title=title, content=content)
            else:
                print('未启用 QQ机器人')
            continue
        elif i == 'pushplus_bot':
            if PUSH_PLUS_TOKEN:
                pushplus_bot(title=title, content=content)
            else:
                print('未启用 PUSHPLUS机器人')
            continue
        elif i == 'wecom_app':
            if QYWX_AM:
                wecom_app(title=title, content=content)
            else:
                print('未启用企业微信应用消息推送')
            continue
        else:
            print('此类推送方式不存在')


def main():
    send('title', 'content')


if __name__ == '__main__':
    main()
