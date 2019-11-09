#!/usr/bin/env python3
# coding=utf-8
# __author__: Alexander
from ..models import *
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(lineno)d - %(funcName)s - %(message)s"  # 时间-级别名称-行号-函数名-信息
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"  # 日期格式
logging.basicConfig(filename='public_function.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def vali_mysql_usr_exists(usr_id, usr_type, usr_school):
    """验证mysql数据库中用户数据是否存在"""
    try:
        if usr_type == 'student':
            StudentInfo.objects.get(student_id=usr_id, school=usr_school)
        elif usr_type == 'teacher':
            TeacherInfo.objects.get(teacher_id=usr_id, school=usr_school)
        return True
    except Exception as e:
        return False


def vali_mysql_data_exists(usr_id, usr_type, usr_school, model):
    """验证mysql中数据是否存在"""
    try:
        model.objects.get(type_id=usr_id, type=usr_type, school=usr_school)
        return True
    except Exception as e:
        logging.debug(e)
        return False


def vali_mysql_info_key(**kwargs):
    """验证密钥"""
    if vali_mysql_usr_exists(**kwargs):
        try:
            if kwargs['usr_type'] == 'student':
                key = StudentInfo.objects.get(student_id=kwargs['usr_id'], school=kwargs['usr_school']).key
            elif kwargs['usr_type'] == 'teacher':
                key = TeacherInfo.objects.get(teacher_id=kwargs['usr_id'], school=kwargs['usr_school']).key
            return key
        except Exception as e:
            return None


def get_mysql_data(usr_id, usr_type, usr_school, model):
    """获取mysql数据，返回queryset，否则返回None"""
    try:
        data_object = model.objects.filter(type_id=usr_id, type=usr_type, school=usr_school)
        return data_object
    except Exception as e:
        logging.debug(e)
        return None


def get_mysql_city(usr_id, usr_type, usr_school):
    """获取城市数量"""
    try:
        datas = get_mysql_data(usr_id, usr_type, usr_school, WechatMap)
        city_data = {}
        for data in datas:
            city_data[data.city] = data.city_count
        return city_data
    except Exception as e:
        logging.debug(e)
        return None


def get_mysql_sex(usr_id, usr_type, usr_school):
    """获取性别数量"""
    try:
        data = WechatSex.objects.get(type_id=usr_id, type=usr_type, school=usr_school)
        sex_data = {}
        sex_data["男"] = data.sex_male
        sex_data["女"] = data.sex_female
        sex_data["其他"] = data.sex_other
        return sex_data
    except Exception as e:
        logging.debug(e)
        return None


def get_mysql_word(usr_id, usr_type, usr_school):
    """获取词频数量"""
    try:
        datas = get_mysql_data(usr_id, usr_type, usr_school, WechatWord)
        datas = datas.order_by('-word_count')
        word_data = {}
        for data in datas:
            word_data[data.word] = data.word_count
        return word_data
    except Exception as e:
        logging.debug(e)
        return None


def get_mysql_map(city, region='中国', state='none'):
    """
    精确查找某个城市经纬度，如果有多条数据取查出来的第一条，不存在的信息缓存进redis,返回数据信息
    :param city: 城市
    :param region: 国家
    :param state: 省、行政区、州
    :return: 经纬度列表[经度，纬度]
    """
    try:
        if state == 'none' and region != 'none':
            data = CityLAL.objects.filter(city=city, country=region).first()
        elif state != 'none' and region == 'none':
            data = CityLAL.objects.filter(city=city, province=state).first()
        elif state != 'none' and region != 'none':
            data = CityLAL.objects.filter(city=city, province=state, country=region).first()
        else:
            data = CityLAL.objects.filter(city=city).first()
        if data.lng == 0 and data.lat == 0:
            class CustomError(Exception):
                pass
            raise CustomError('自定义异常，'+city+',该城市不存在，标识坐标为[0,0]')
        return [data.lng, data.lat]
    except Exception as e:
        logging.debug(e)
        from .redis_operate import create_redis_map_not_exists, exists_redis_map_not_exists
        if exists_redis_map_not_exists(city=city, state=state, region=region) is False:  # 在redis不存在列表不存在
            create_redis_map_not_exists(city=city, state=state, region=region)
            logging.warning(city + ',' + state+','+region + '不存在')
            return None


def get_all_mysql_map(city_names, region='none', state='none'):
    """
    获取城市列表中所有经纬度信息
    :param city_names: 城市列表
    :param region: 国家
    :param state: 省、行政区、州
    :return: 经纬度字典
    """
    try:
        datas = {}
        for city in city_names:
            try:
                datas[city] = get_mysql_map(city=city, region=region, state=state)
            except Exception as e:
                continue
        return datas
    except Exception as e:
        logging.debug(e)
        return None

