#!/usr/bin/env python3
# coding=utf-8
# __author__: Alexander
from celery import task
from .plugin import redis_config, redis_operate
from .models import *
import datetime
import json


def set_redis_value_exist(name):
    """将用户数据转为‘exist’"""
    try:
        redis_config.redis_sr.set(name=name, value='exist')
        return True
    except Exception as e:
        print(e)
        return False


def base_info_save(base_info, model_name):
    """保存基础信息"""
    base_info['date'] = str(datetime.datetime.now().date())
    base_info.pop('type')
    base_info.pop('id')
    try:
        model_name.objects.create(**base_info)
        flag = True
    except Exception:
        flag = False
    return flag


def data_city_save(data, model_name, type_name, type_id, school_name):
    """保存城市分布信息"""
    flag = False
    city_counts = json.loads(data)
    for city in city_counts.keys():
        city_counts_dict = {'type': type_name,
                            'type_id': type_id,
                            'school': school_name,
                            'city': city,
                            'city_count': city_counts.get(city)}
        try:
            model_name.objects.create(**city_counts_dict)
            flag = True
        except Exception:
            return False
    return flag


def data_signature_save(data, model_name, type_name, type_id, school_name):
    '''
    保存词频数据
    :param data: 数据
    :param model_name: model名称
    :param type_name: 类型
    :param type_id: 学号或其他号
    :param school_name: 学院名称
    :return: 是否保存成功
    '''
    flag = False
    word_counts_dict = json.loads(data)
    for word in word_counts_dict.keys():  # 遍历键
        word_counts = {'type': type_name,
                       'type_id': type_id,
                       'school': school_name,
                       'word': word,
                       'word_count': word_counts_dict.get(word)}
        try:
            model_name.objects.create(**word_counts)
            flag = True
        except Exception:
            return False
    return flag


def data_sex_save(data, model_name, type_name, type_id, school_name):
    """保存性别数据"""
    sex_counts = json.loads(data)
    sex_counts['type'] = type_name
    sex_counts['type_id'] = type_id
    sex_counts['school'] = school_name
    sex_counts['sex_other'] = sex_counts['0']
    sex_counts['sex_male'] = sex_counts['1']
    sex_counts['sex_female'] = sex_counts['2']
    sex_counts.pop('0')
    sex_counts.pop('1')
    sex_counts.pop('2')
    try:
        model_name.objects.create(**sex_counts)
    except Exception:
        return False
    return True


@task()
def redis_to_mysql():
    """定期将redis用户数据存入mysql"""
    print('开始执行定时任务redis_to_mysql,'+str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")))
    names = redis_config.redis_sr.keys()
    for name in names:
        try:
            if redis_config.redis_sr.get(name) == 'exist':
                continue
        except Exception:
            pass
        base_info = redis_config.redis_sr.hget(name=name, key='base_info')
        base_info = json.loads(base_info)
        base_info['key'] = redis_operate.get_redis_key(name=name)
        type_name = base_info['type']
        type_id = base_info['id']
        if base_info['type'] == 'student':
            base_info['student_id'] = base_info['id']
            info_save = base_info_save(base_info, StudentInfo)
        else:
            base_info['teacher_id'] = base_info['id']
            info_save = base_info_save(base_info, TeacherInfo)
        if info_save:
            data = redis_config.redis_sr.hget(name=name, key='data')
            data = json.loads(data)
            pattern = {
                'type_name': type_name,
                'type_id': type_id,
                'school_name': base_info['school']
            }
            city_save = data_city_save(data=data['city'],
                                       model_name=WechatMap, **pattern)
            signature_save = data_signature_save(data=data['signature'],
                                                 model_name=WechatWord, **pattern)
            sex_save = data_sex_save(data=data['sex'],
                                     model_name=WechatSex,
                                     **pattern)

            if city_save and signature_save and sex_save:
                set_redis_value_exist(name)
                print(name+'保存成功，'+str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")))
            else:
                print(name + '保存失败，' + str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")))
        else:
            print(name + '保存失败，' + str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")))
