# Generated by Django 2.1 on 2018-12-23 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0003_auto_20181205_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='key',
            field=models.CharField(default='123alex', max_length=10),
        ),
        migrations.AddField(
            model_name='teacherinfo',
            name='key',
            field=models.CharField(default='123alex', max_length=10),
        ),
    ]