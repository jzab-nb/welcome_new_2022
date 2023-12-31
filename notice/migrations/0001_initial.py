# Generated by Django 3.2 on 2022-09-17 11:58

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeadPhoto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='主键')),
                ('image', models.ImageField(default='static/none.jpg', upload_to='static/notice/lbt', verbose_name='图片')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='主键')),
                ('title', models.CharField(max_length=30, verbose_name='标题')),
                ('content', models.TextField(blank=True, null=True, verbose_name='正文')),
                ('time', models.DateField(default=datetime.datetime(2022, 9, 17, 19, 58, 1, 823972), verbose_name='上传日期')),
                ('author', models.CharField(default='信息工程学院', max_length=30, verbose_name='作者')),
                ('radio', models.BooleanField(default=True, verbose_name='是否广播')),
            ],
        ),
        migrations.CreateModel(
            name='NoticeStudent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='主键')),
                ('read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('notice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notice.notice')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='NoticeImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='主键')),
                ('image', models.ImageField(default='static/none.jpg', upload_to='static/notice/notice', verbose_name='图片')),
                ('notice', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='notice.notice')),
            ],
        ),
    ]
