#!/usr/bin/env python3
# coding=utf-8
# __author__: Alexander
import itchat, time, logging, random
import pandas as pd
import json
import jieba
import re

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(lineno)d - %(funcName)s - %(message)s"  # 时间-级别名称-行号-函数名-信息
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"  # 日期格式
logging.basicConfig(filename='public_function.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def city_count(df):
    df2 = df[df['City'] != '']
    df2['City'][df2['Province'] == u'北京'] = u'北京'
    df2['City'][df2['Province'] == u'上海'] = u'上海'
    df2['City'][df2['Province'] == u'重庆'] = u'重庆'
    df2['City'][df2['Province'] == u'天津'] = u'天津'
    df2['City'][df2['Province'] == u'香港'] = u'香港'
    df2['City'][df2['Province'] == u'澳门'] = u'澳门'
    city = df2.City
    counts = city.value_counts()
    return counts.to_json(force_ascii=False)


def sex_count(data_frame):
    sex = data_frame.Sex
    counts = sex.value_counts()
    return counts.to_json(force_ascii=False)


def signatureStatistic(data_frame):
    """词频统计"""
    signatures = data_frame.Signature
    text = u''
    for signature in signatures:
        signature = signature.strip().replace('emoji', '').replace('span', '').replace('class', '').replace('"', '')
        rep = re.compile('1f\d+\w*|[<>/=]')
        signature = rep.sub('', signature)
        if len(signature) > 0:
            text += signature
    text = text.replace('\n', '')
    wordlist = jieba.cut(text, cut_all=True)
    # word_space_split = " ".join(wordlist)
    df_word = pd.DataFrame(wordlist)
    word_count = df_word[0].value_counts()
    return word_count.to_json(force_ascii=False)


def start(instance):
    """
    开始爬取数据
    :param instance: 实例
    :return: 爬取状态，200爬取成功
    """
    friends = instance.get_friends(update=True)[0:]
    data = {}
    df_friends = pd.DataFrame(friends)
    data['city'] = city_count(df_friends)
    data['sex'] = sex_count(df_friends)
    data['signature'] = signatureStatistic(df_friends)
    return data


def login(instance, session_id):
    def open_QR(instance, session_id):
        for get_count in range(10):
            uuid = instance.get_QRuuid()
            uuid_count = 0
            while uuid is None:
                if uuid_count == 9:
                    logging.error("uuid请求超时!!请检查网络，或者ip被封，session_id:" + session_id)
                    break
                uuid = instance.get_QRuuid()
                time.sleep(1)
                uuid_count = uuid_count + 1
            if instance.get_QR(uuid=uuid,
                               picDir='/home/alex/www/spider_data/static/img/qr/' + session_id + '.png'):
                break
            elif get_count >= 9:
                logging.debug("二维码请求超时!!session_id:" + session_id)
                return None  # 退出
        return uuid

    uuid = open_QR(instance, session_id)
    if uuid is None:
        return False
    waitForConfirm = False
    count = 0
    while 1:
        if count >= 3:
            logging.debug("二维码失效三次！session_id:" + session_id)
            return False  # 如果二维码失效次数超过三次就退出
        status = instance.check_login(uuid)
        if status == '200':  # 成功登录
            break
        elif status == '201':  # 已扫描二维码
            if waitForConfirm:
                waitForConfirm = True
        elif status == '408':  # 二维码失效
            uuid = open_QR(instance, session_id)
            waitForConfirm = False
            count = count + 1
    instance.web_init()  # 获取登录用户初始信息
    instance.show_mobile_login()  # 在手机上显示登录状态
    instance.send('来自Alexander数据采集网的信息：正在采集数据，请稍等...', toUserName='filehelper')
    msg = start(instance)
    key = session_id.split('.')
    character = ['a', '7', 'b', 'c', 'x', 'z', '4', '9', 'E', 'A', 'B', 'C']
    key = character[random.randint(0, 11)] + \
          key[1] + \
          character[random.randint(0, 11)] + \
          character[random.randint(0, 11)]  # 生成查询密钥
    instance.send('来自Alexander数据采集网的信息：数据采集成功！您的个人数据查询密钥为：' + key, toUserName='filehelper')
    msg['key'] = key
    return msg


def instance_save(session_id):
    try:
        itchat.new_instance_dict(session_id)
        return True
    except Exception as e:
        print(e)
        return False


def main_control(session_id):
    newInstance = itchat.restore_instance(session_id)
    msg = login(newInstance, session_id)
    return msg


if __name__ == '__main__':
    print(json.loads(json.dumps(main_control(), ensure_ascii=False)))
    # print()
