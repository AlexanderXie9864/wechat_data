from django.views.decorators.csrf import csrf_exempt
from .plugin import redis_config, spider_itchat, mysql_operate, redis_operate
from django.http.response import HttpResponse
import time, random, logging
from django.shortcuts import render, redirect
from .models import *
import json
# Create your views here.


def data_acquisition_index(request):
    """数据采集首页面"""
    # temp=loader.get_template('bookapp/index.html')
    # return HttpResponse(temp.render())
    if request.method == "GET":
        if request.session.get('session_id', None) is None:  # 如果没有session_id,则创建session
            request.session['session_id'] = time.strftime("%y%m%d%H%M%S", time.localtime()) + str(round(random.random(),3))
        return render(request, 'wechat/da.html')
    else:
        return HttpResponse('请求失败！')


def data_acquisition_student_info(request):
    """数据采集,学生基本信息"""
    if request.method == "GET":
        if request.session.get('session_id', None) is None:  # 如果没有session_id,则返回首页
            return redirect('/')
        session_id = request.session['session_id']
        context = {
            'session_id': session_id,
        }
        return render(request, 'wechat/studentinfo.html', context=context)
    else:
        return HttpResponse('请求失败！')


def data_acquisition_teacher_info(request):
    """数据采集,老师基本信息"""
    if request.method == "GET":
        if request.session.get('session_id', None) is None:  # 如果没有session_id,则返回首页
            return redirect('/')
        session_id = request.session['session_id']
        context = {
            'session_id': session_id,
        }
        return render(request, 'wechat/teacherinfo.html',  context=context)
    else:
        return HttpResponse('请求失败！')


@csrf_exempt
def data_acquisition_info_save(request):
    if request.method == "POST":
        if request.session.get('session_id', None) is None:  # 如果没有session_id,则返回首页
            return redirect("/")
        data = {}  # post数据
        session_id = request.session['session_id']
        try:
            data['id'] = request.POST['student_id']
            data['type'] = 'student'
        except Exception:
            data['id'] = request.POST['teacher_id']
            data['type'] = 'teacher'
        data['sex'] = request.POST['sex']
        data['school'] = request.POST['school']
        data['department'] = request.POST['department']
        if data['type'] == 'student':
            data['enrollment_year'] = request.POST['eroyear']
            data['major'] = request.POST['major']
        if spider_itchat.instance_save(session_id):  # 为当前用户创建实例
            try:
                msg = spider_itchat.main_control(session_id)
            except Exception as e:
                logging.debug(e)
        else:
            logging.error('当前用户实例创建失败，session_id: '+session_id)
            return render(request, 'wechat/da_fail.html')
        if msg is not False:
            name = data['id'] + ',' + data['type'] + ',' + data['school']
            set_success = redis_config.redis_sr.hset(name=name,
                                                     key='data',
                                                     value=json.dumps(msg, ensure_ascii=False))  # 提取数据存入redis
            if set_success:
                set_success = redis_config.redis_sr.hset(name=name,
                                                         key='base_info',
                                                         value=json.dumps(data, ensure_ascii=False))
                if set_success:
                    contex = {
                        "usr_id": data['id'],
                        "usr_type": data['type'],
                        "usr_school": data['school'],
                        "key": msg['key']
                    }
                    return render(request, 'wechat/da_success.html', context=contex)
            logging.error('数据采集失败，数据未正常入库redis，session_id: '+session_id)

        logging.error('数据采集失败，session_id: ' + session_id)
        return render(request, 'wechat/da_fail.html')
    else:
        return HttpResponse('请求失败！')


@csrf_exempt
def data_acquisition_info_check(request):
    if request.method == "POST":
        if request.session.get('session_id', None) is None:  # 如果没有session_id,则返回首页
            return redirect("/")
        # print('data_acquisition_info_check:当前用户id='+request.session['session_id'])
        data = request.body.decode('utf8')
        data = json.loads(data)
        redis_info_key = redis_config.redis_sr.exists(data['id']+','+data['type']+','+data['school'])

        if redis_info_key is not True:  # redis中不存在

            if mysql_operate.vali_mysql_usr_exists(usr_id=data['id'],
                                                   usr_type=data['type'],
                                                   usr_school=data['school']):  # 如果存在
                response = {'msg': 'exist'}
                return HttpResponse(json.dumps(response))
            else:

                response = {'msg': 'success'}
                return HttpResponse(json.dumps(response))
        response = {'msg': 'exist'}
        return HttpResponse(json.dumps(response))
    else:
        return HttpResponse('请求失败！')


def data_acquisition_show(request):
    """数据采集,用户个人数据展示"""
    if request.method == "GET":
        if request.session.get('session_id', None) is None:  # 如果没有session_id,则返回首页
            return redirect('/')
        usr_id = request.GET.get('id', None)
        usr_type = request.GET.get('type', None)
        usr_school = request.GET.get('school', None)
        key = request.GET.get('key', None)
        if usr_id != '' and usr_type != '' and usr_school != '' and key != '':
            name = usr_id+','+usr_type+','+usr_school
            try:
                redis_ex = redis_config.redis_sr.hexists(name=name, key='data')
            except Exception as e:
                print(e)
                redis_ex = False
            if not redis_ex:  # 如果redis中不存在
                if mysql_operate.vali_mysql_info_key(usr_id=usr_id,
                                                     usr_type=usr_type,
                                                     usr_school=usr_school) == key:  # 在mysql中存在,且key值验证成功

                    data_city = mysql_operate.get_mysql_city(usr_id=usr_id,
                                                             usr_type=usr_type,
                                                             usr_school=usr_school)
                    data_word = mysql_operate.get_mysql_word(usr_id=usr_id,
                                                             usr_type=usr_type,
                                                             usr_school=usr_school)

                    data_sex = mysql_operate.get_mysql_sex(usr_id=usr_id,
                                                           usr_type=usr_type,
                                                           usr_school=usr_school)
                    data_word.pop('')
                    data_word.pop('的')
                    data_map = mysql_operate.get_all_mysql_map(data_city.keys())
                    context = {
                        'data_city': json.dumps(data_city, ensure_ascii=False),
                        'data_sex': json.dumps(data_sex, ensure_ascii=False),
                        'data_word': json.dumps(data_word, ensure_ascii=False),
                        'data_map': json.dumps(data_map, ensure_ascii=False)
                    }
                    return render(request, 'wechat/wechat_analysis.html', context=context)

                return HttpResponse('未找到相关数据，或者查询密钥错误！')

            else:
                pattern = {
                    'type_id': usr_id,
                    'type_name': usr_type,
                    'school_name': usr_school
                }
                if key != redis_operate.get_redis_key(**pattern):
                    return HttpResponse('未找到相关数据，或者查询密钥错误！')
                data_city = redis_operate.get_redis_city(**pattern)
                data_word = redis_operate.get_redis_word(**pattern)
                data_sex = redis_operate.get_redis_sex(**pattern)
                data_word.pop('')
                data_word.pop('的')
                data_map = mysql_operate.get_all_mysql_map(city_names=data_city.keys())
                context = {
                    'data_city': json.dumps(data_city, ensure_ascii=False),
                    'data_sex': json.dumps(data_sex, ensure_ascii=False),
                    'data_word': json.dumps(data_word, ensure_ascii=False),
                    'data_map': json.dumps(data_map, ensure_ascii=False)
                }
                return render(request, 'wechat/wechat_analysis.html', context=context)
                # return HttpResponse('未找到相关数据！')
        return redirect('/da/daSearch')
    else:
        return HttpResponse('请求失败！')


def data_acquisition_search(request):
    if request.method == "GET":
        if request.session.get('session_id', None) is None:  # 如果没有session_id,则返回首页
            return redirect('/')
        return render(request, 'wechat/da_search.html')
    else:
        return HttpResponse('请求失败！')