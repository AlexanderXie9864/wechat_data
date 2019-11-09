from django.db import models


# Create your models here.
class CityLAL(models.Model):
    """城市经纬度表"""
    id = models.AutoField(primary_key=True)
    city = models.CharField(default='none', max_length=200)
    lng = models.FloatField(null=False)  # 经度
    lat = models.FloatField(null=False)  # 纬度
    province = models.CharField(max_length=200)
    country = models.CharField(null=False, max_length=20, default='中国')  # 用中文


class StudentInfo(models.Model):
    """用户信息表"""
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(null=False, max_length=20)
    sex = models.CharField(null=False, max_length=2)
    school = models.CharField(null=False, max_length=20)
    department = models.CharField(null=False, max_length=20)
    major = models.CharField(null=False, max_length=20)
    enrollment_year = models.CharField(null=False, max_length=5)
    date = models.CharField(null=False, max_length=10)
    key = models.CharField(null=False, max_length=10, default='123alex')


class TeacherInfo(models.Model):
    """教师信息表"""
    id = models.AutoField(null=False, primary_key=True)
    teacher_id = models.CharField(null=False, max_length=20)
    sex = models.CharField(null=False, max_length=2)
    school = models.CharField(null=False, max_length=20)
    department = models.CharField(null=False, max_length=20)
    date = models.CharField(null=False, max_length=10)
    key = models.CharField(null=False, max_length=10, default='123alex')

class WechatSex(models.Model):
    """微信性别数据表"""
    type_id = models.CharField(null=False, max_length=20, default='none')
    type = models.CharField(null=False, max_length=8)  # 用于检索
    school = models.CharField(null=False, max_length=20)  # 用于精确检索
    sex_male = models.IntegerField(null=False, default=0)
    sex_female = models.IntegerField(null=False, default=0)
    sex_other = models.IntegerField(null=False, default=0)


class WechatMap(models.Model):
    """微信人口分布数据表"""
    type_id = models.CharField(null=False, max_length=20, default='none')
    type = models.CharField(null=False, max_length=8)  # 用于检索
    school = models.CharField(null=False, max_length=20)  # 用于精确检索
    city = models.CharField(null=False, max_length=20)
    city_count = models.IntegerField(null=False)
    province = models.CharField(null=False, max_length=20, default='none')
    country = models.CharField(null=False, max_length=10, default='none')


class WechatWord(models.Model):
    """微信好友签名词频统计表"""
    type_id = models.CharField(null=False, max_length=20, default='none')
    type = models.CharField(null=False, max_length=8)  # 用于检索
    school = models.CharField(null=False, max_length=20)  # 用于精确检索
    word = models.CharField(null=False, max_length=20)
    word_count = models.IntegerField(null=False)
