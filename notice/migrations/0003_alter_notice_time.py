# Generated by Django 3.2 on 2022-09-18 02:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0002_alter_notice_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='time',
            field=models.DateField(default=datetime.datetime.now, verbose_name='上传日期'),
        ),
    ]