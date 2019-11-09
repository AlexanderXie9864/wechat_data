# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 12:14:22 2018

@author: xb
"""

import pymysql as pm
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from config import *

conn = pm.connect(**connect_dic)  # 连接数据库

def population():
    '''人数统计'''
    print('***********************被采集用户数据分析*************************')
    df_student = pd.read_sql(student_sql,conn)
    df_teacher = pd.read_sql(teacher_sql,conn)
    
    """**********人数**********"""
    student_count = df_student['student_id'].count()
    teacher_count = df_teacher['teacher_id'].count()
    
    """**********学校**********"""
#    student_school = df_student['school']
#    student_school_des = student_school.describe()
#    teacher_school = df_teacher['school']
#    teacher_school_des = teacher_school.describe()
#    
#    student_school_top = student_school_des['top']
#    student_school_top_count = student_school[student_school==student_school_des['top']].count()
#    teacher_school_top = teacher_school_des['top']
#    teacher_school_top_count = teacher_school[teacher_school==teacher_school_des['top']].count()
    
    
    
    """**********性别**********"""
    student_sex = df_student['sex']
    student_sex_des = student_sex.describe()
    teacher_sex = df_teacher['sex']
    teacher_sex_des = teacher_sex.describe()
    
    student_sex_count = student_sex.value_counts()
    teacher_sex_count = teacher_sex.value_counts()
    
    student_sex_top = student_sex_des['top']
    teacher_sex_top = teacher_sex_des['top']
    
    
    
    """*********学生数据打印*******"""
    print('共采集学生数据'+str(student_count)+'人')
    print('其中，'+student_sex_top+'性人数最多，共有'+str(student_sex_count[student_sex_top])+'人')
    print(student_sex_count)
    
    """*********教师数据打印*******"""
    print('共采集教师数据'+str(teacher_count)+'人')
    print('其中，'+teacher_sex_top+'性人数最多，共有'+str(teacher_sex_count[teacher_sex_top])+'人')
    print(teacher_sex_count)
    
def city_analysis():
    '''城市数据清理及分析'''
    df = pd.read_sql(city_sql,conn)
    df=df.loc[:,['city','city_count']]
    df=df.sort_values(['city_count'],ascending=False)  # 降序排列
    label = df.drop_duplicates(['city'])
    label = list(label.city)
    
    print('***********************城市数据分析1*************************')
    city_value = []
    for la in label:
        city_value.append((la,df[df.city==la].city_count.sum()))
    print('城市好友总人数数据总览：')
    city_value = pd.DataFrame(city_value).sort_values([1],ascending=False)
    print(city_value) 
    values = city_value[1][0:10]
    labels = city_value[0][0:10]
    explodes = [0 for x in values]
    explodes[0] = 0.05
    pie=plt.pie(values,
                labels=labels,
                #autopct='%1.1f%%',
                autopct='%.1f%%',
                startangle=45,
                explode=explodes,
                wedgeprops=dict(width=0.6,edgecolor='w'),
               
                )
    #按百分数显示扇形图
    plt.legend(prop=fontset,
               borderaxespad=0.3,
               loc='upper right',
               shadow=True,
               markerfirst=False,
               bbox_to_anchor=(1.2, 1.05),  #外边距 上边 右边
               )
    
    for font in pie[1]:
        font.set_fontproperties(fontset)
    plt.axis('equal')
    #使饼状图长宽相等
    plt.title('人数最多的10个城市人数占比',fontproperties=fontset,fontsize=20)
    plt.show()
    print('\t')
    
    print('***********************城市数据分析2*************************')
    print('好友最多的前十个城市以及拥有该城市好友的用户人数')
    value_count = df['city'].value_counts()
    count = value_count.count()  # 共统计城市个数
    print("共统计城市个数:",count)
    
    # 好友最多的前十个城市以及拥有该城市好友的用户人数
    value=[]
    for index in value_count.index:
        value.append((index,value_count[index]))
        
    print('好友最多的前十个城市以及拥有该城市好友的用户人数总览')
    value=pd.DataFrame(value).sort_values([1],ascending=False)
    print(value)
    explodes = [0 for x in range(0,10)]
    explodes[0] = 0.05
    
    values = value[1][0:10]
    labels = value[0][0:10]
    pie=plt.pie(values,
                labels=labels,
                #autopct='%1.1f%%',
                autopct='%.1f%%',
                startangle=45,
                labeldistance = 1.1,
                pctdistance = 0.6,
                explode=explodes,
                wedgeprops=dict(width=0.6,edgecolor='w'),
               
                )
    #按百分数显示扇形图
    plt.legend(prop=fontset,
               shadow=True,
               markerfirst=False,
               bbox_to_anchor=(1.2, 1.05),  #外边距 上边 右边
               )
    
    for font in pie[1]:
        font.set_fontproperties(fontset)
    plt.axis('equal')
    #使饼状图长宽相等
    plt.title('拥有城市好友用户数最多的10个城市占比',fontproperties=fontset,fontsize=20)
    plt.show()
    
def word_count():
    '''词频统计'''
    df_word = pd.read_sql(word_sql,conn)
    df_word=df_word.loc[:,['word','word_count']]
    df_word_count = df_word['word'].value_counts()
    print('对于所有被采集的用户出现次数最多的前20个词，以及其次数:')
    print(df_word_count[0:20])
    word_count_list = {}
    for word in df_word_count.index:
        word_count_list[word]=df_word[df_word.word==word].word_count.sum()
    #word_count = pd.DataFrame(word_count_list).sort_values([1],ascending=False)
    print('对于所有被采集的用户好友出现次数最多的前20个词，以及其次数:')
    print(word_count_list)

def sex_count():
    '''性别比例'''
    df_sex = pd.read_sql(sex_sql,conn)
    df_sex = df_sex.loc[:,['sex_male','sex_female','sex_other']]
    df_male_count = df_sex['sex_male'].sum()
    df_female_count = df_sex['sex_female'].sum()
    df_other_count = df_sex['sex_other'].sum()
    print('共提取了（包括被采集用户）:'+str(df_male_count+df_female_count+df_other_count)+'个人的数据')
    print('对于所有被采集的用户好友性别比例:')
    print('男：'+str(df_male_count))
    print('女：'+str(df_female_count))
    print('不明：'+str(df_other_count))
    data = [('男',df_male_count),('女',df_female_count),('不明',df_other_count)]
    data = pd.DataFrame(data)
    
    values = data[1]
    labels = data[0]
    pie=plt.pie(values,
                labels=labels,
                #autopct='%1.1f%%',
                autopct='%.1f%%',
                startangle=45,
                labeldistance = 1.1,
                pctdistance = 0.6,
                wedgeprops=dict(width=0.6,edgecolor='w'),
               
                )
    #按百分数显示扇形图
    
    plt.legend(prop=fontset,
               shadow=True,
               markerfirst=False,
               )
    
    for font in pie[1]:
        font.set_fontproperties(fontset)
    plt.axis('equal')
    #使饼状图长宽相等
    plt.title('所有用户好友性别比例',fontproperties=fontset,fontsize=20)
    plt.show()
if __name__ == '__main__':
#    population()
#    city_analysis()
    word_count()
#    sex_count()