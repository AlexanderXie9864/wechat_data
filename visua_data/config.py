# -*- coding: utf-8 -*-

connect_dic = {
        'host': '',
        'user': 'root',
        'passwd': '',
        'db': 'wechat_data',
        'charset': 'utf8',
        'port': 3306
        }
city_sql = "SELECT * FROM wechat_wechatmap"
sex_sql = "SELECT * FROM wechat_wechatsex"
word_sql = "SELECT * FROM wechat_wechatword where word!='的'"
student_sql = "SELECT * FROM wechat_studentinfo"
teacher_sql = "SELECT * FROM wechat_teacherinfo"

fontset=mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')