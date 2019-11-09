from django.contrib import admin
from .models import StudentInfo
from .models import TeacherInfo
from .models import CityLAL
from .models import WechatSex, WechatMap, WechatWord
# Register your models here.


class MyAdminSite(admin.AdminSite):
    site_header = "Wechat数据分析后台管理"
    site_title = "后台管理"


admin_site = MyAdminSite(name='admin')


@admin.register(StudentInfo)
class StudentInfoAdmin(admin.ModelAdmin):
    """学生信息表后台"""
    list_display = ('student_id', 'school', 'department', 'major', 'enrollment_year')
    # 根据字段进行查找
    search_fields = ('studen_id', 'school')
    # 指定列表过滤器
    list_filter = ('school', 'department', 'major', 'enrollment_year')
    # 如果不加，会默认按照id降序进行排列，加上按照升序
    # 如果在id之前加上 '-'，则按照降序
    ordering = ('enrollment_year',)
    # 指定需要编辑的字段
    # fields = ('name', 'city')
    # 指定不需要编辑的字段
    exclude = ('student_id',)
    # 设置分组表单,下面代码中一共分了两组，
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'city',)
    #     }),
    #     ('Advanced options', {
    #         'classes': ('collapse',),
    #         'fields': ('country', 'address'),
    #     }),
    # )


@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    """教师信息表后台"""
    list_display = ('teacher_id', 'school', 'department')
    # 根据字段进行查找
    search_fields = ('teacher_id', 'school',)
    # 指定列表过滤器
    list_filter = ('school', 'department')
    # 如果不加，会默认按照id降序进行排列，加上按照升序
    # 如果在id之前加上 '-'，则按照降序
    ordering = ('school',)
    # 指定需要编辑的字段
    # fields = ('name', 'city')
    # 指定不需要编辑的字段
    exclude = ('teacher_id',)


@admin.register(CityLAL)
class CityLALAdmin(admin.ModelAdmin):
    list_display = ('city', 'lng', 'lat', 'province', 'country')
    # 根据字段进行查找
    search_fields = ('city', 'province', 'country')
    # 指定列表过滤器
    # 如果不加，会默认按照id降序进行排列，加上按照升序
    # 如果在id之前加上 '-'，则按照降序
    ordering = ('city',)