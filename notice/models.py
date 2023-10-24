from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from student.models import Student
import uuid, datetime

class HeadPhoto(models.Model):
    UPLOAD_TO = 'static/notice/'
    DEFAULT = 'static/none.jpg'
    id = models.UUIDField("主键", default=uuid.uuid4, primary_key=True)
    image = models.ImageField("图片", upload_to=UPLOAD_TO+'lbt', default=DEFAULT)

class Notice(models.Model):
    id = models.UUIDField("主键", default=uuid.uuid4, primary_key=True)
    title = models.CharField("标题", max_length=30)
    content = models.TextField("正文", null=True, blank=True)
    time = models.DateField("上传日期", default=datetime.datetime.now, editable=True)
    author = models.CharField("作者", max_length=30, default="信息工程学院")
    radio = models.BooleanField("是否广播", default=True)

    def img(self):
        lst = []
        for i in self.noticeimage_set.all():
            lst.append(i.image.name)
        return lst

    def __str__(self):
        return self.title

class NoticeImage(models.Model):
    UPLOAD_TO = 'static/notice/'
    DEFAULT = 'static/none.jpg'
    id = models.UUIDField("主键", default=uuid.uuid4, primary_key=True)
    image = models.ImageField("图片", upload_to=UPLOAD_TO+'notice', default=DEFAULT)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, default=None)

class NoticeStudent(models.Model):
    id = models.UUIDField("主键", default=uuid.uuid4, primary_key=True, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    read = models.BooleanField("是否已读", default=False)

@receiver(post_save, sender=Notice)
def create_ns1(sender, instance=None, created=False, **kwargs):
    if created and instance.radio is True:
        for sid in Student.objects.all():
            NoticeStudent.objects.create(student_id=sid.uuid, notice_id=instance.id)

@receiver(post_save, sender=Student)
def create_ns2(sender, instance=None, created=False, **kwargs):
    if created:
        for nid in Notice.objects.filter(radio=True):
            NoticeStudent.objects.create(student_id=instance.uuid, notice_id=nid.id)
