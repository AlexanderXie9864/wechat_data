#!/usr/bin/env python3
# coding=utf-8
# __author__: Alexander
from django.urls import path
from . import views


urlpatterns = [
    path('', views.data_acquisition_index),
    path('da/studentInfor', views.data_acquisition_student_info),
    path('da/teacherInfor', views.data_acquisition_teacher_info),
    path('da/infoCheck', views.data_acquisition_info_check),
    path('da/infoSave', views.data_acquisition_info_save),
    path('da/dataPerShow', views.data_acquisition_show),
    path('da/daSearch', views.data_acquisition_search),
    # path('register/', views.register),
    # path('logout/', views.logout),
    # path('index/getService/', views.get_service),
    # path('index/getFamilyKit/', views.get_familykit),
    # path('index/download/', views.download)
]
