#!/usr/bin/env python3
# coding=utf-8
# __author__: Alexander
from .redis_config import redis_sr, redis_map
import logging
import json

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(lineno)d - %(funcName)s - %(message)s"  # 时间-级别名称-行号-函数名-信息
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"  # 日期格式
logging.basicConfig(filename='public_function.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def get_redis_data(name, data_type):
    """
    获取redis中用户的data信息数据
    :param name:redis的key
    :param data_type:获取数据类型
    :return: 对应数据的dict
    """
    data = redis_sr.hget(name=name, key='data')
    if data:
        data = json.loads(data)
        return data[data_type]


def get_redis_city(type_name, type_id, school_name):
    """获取城市分布信息"""
    name = type_id+','+type_name+','+school_name
    data = get_redis_data(name, 'city')
    city_counts = json.loads(data)
    city_counts_dict = {}
    for city in city_counts.keys():
        city_counts_dict[city] = city_counts.get(city)
    return city_counts_dict


def get_redis_province(type_name, type_id, school_name):
    """获取省份分布信息"""
    name = type_id+','+type_name+','+school_name
    data = get_redis_data(name, 'province')
    province_counts = json.loads(data)
    province_counts_dict = {}
    for province in province_counts.keys():
        province_counts_dict[province] = province_counts.get(province)
    return province_counts_dict


def get_redis_province_list(usr_id, usr_type, usr_school):
    """
    从redis获取好友省份名称列表
    :param usr_id: 用户id
    :param usr_type: 用户类型
    :param usr_school: 用户学校
    :return: 省份名称列表
    """
    province = get_redis_province(type_name=usr_type, type_id=usr_id, school_name=usr_school)
    province_list = []
    for p in province.keys():
        province_list.append(p)
    return province_list


def get_redis_sex(type_name, type_id, school_name):
    """获取性别信息"""
    name = type_id+','+type_name+','+school_name
    data = get_redis_data(name, 'sex')
    sex_counts = json.loads(data)
    sex_counts_dict = {}
    sex_counts_dict['其他'] = sex_counts['0']
    sex_counts_dict['男'] = sex_counts['1']
    sex_counts_dict['女'] = sex_counts['2']
    return sex_counts_dict


def get_redis_word(type_name, type_id, school_name):
    """获取词频信息"""
    name = type_id+','+type_name+','+school_name
    data = get_redis_data(name, 'signature')
    word_counts = json.loads(data)
    word_counts_dict = {}
    for word in word_counts.keys():
        word_counts_dict[word] = word_counts.get(word)
    return word_counts_dict


def get_redis_key(type_name=None, type_id=None, school_name=None, name=None):
    """获取密钥"""
    if name is None:
        name = type_id+','+type_name+','+school_name
    data = get_redis_data(name, 'key')
    return data


def get_redis_map_lal_exists(city, state='none', region='none'):
    """获取存在经纬度信息的数据"""
    key = city + ',' + state + ',' + region
    try:
        lal = redis_map.hget(name='exists', key=key)
        lal = list(lal)
        return lal
    except Exception as e:
        logging.warning(e)
        return None


def create_redis_map_lal_exists(city, lal, state='none', region='none'):
    """创建有经纬度的数据"""
    key = city + ',' + state + ',' + region
    try:
        redis_map.hset(name='exists', key=key, value=lal)
        return True
    except Exception as e:
        logging.error(e)
        return False


def get_all_redis_map_not_exists():
    """获取所有不存在经纬度的城市名和国家"""
    try:
        city = redis_map.get(name='not_exists')
        return city
    except Exception as e:
        logging.warning(e)
        return None


def get_redis_map_not_exists_by_region(region='none'):
    """根据国家地区获取不存在经纬度数据的城市列表"""
    try:
        lis = get_all_redis_map_not_exists()
    except Exception as e:
        logging.warning(e)
        return None
    city_list = []
    for city in lis:
        city_region = city.split(',')
        if city_region[2] == region:
            city_list.append(city_region[0])
    return city_list


def exists_redis_map_not_exists(city, state='none', region='none'):
    """验证是否有该不存在经纬度数据的城市"""
    try:
        key = city+','+state+','+region
        if redis_map.hexists(name='not_exists', key=key):
            return True
        else:
            return False
    except Exception as e:
        logging.debug(e)
        return 'error'


def create_redis_map_not_exists(city, state='none', region='none'):
    """创建不存在经纬度的数据，value为none"""
    key = city + ',' + state + ',' + region
    try:
        redis_map.hset(name='not_exists', key=key, value='none')
        return True
    except Exception as e:
        logging.error(e)
        return False

