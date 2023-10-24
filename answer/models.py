from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from student.models import Student
import uuid, json, random

# Create your models here.
class Question(models.Model):
    title = models.TextField("题干")
    choice = models.TextField("选项")
    answer = models.IntegerField("答案")

class Test(models.Model):
    uuid = models.UUIDField("主键", default=uuid.uuid4, primary_key=True)
    questions = models.TextField("关联的题目类")

class StudentTest(models.Model):
    uuid = models.UUIDField("主键", default=uuid.uuid4, primary_key=True)
    # [
    #   [0,2,3,1],
    #   [1,2,3,0],
    #   ...
    # ]
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    choice = models.TextField("选项的乱序")
    # [0,1,2,3]
    answer = models.TextField("新组成的答案列表")
    is_pass = models.BooleanField("是否通过", default=False)

def create_st(student, test):
    choice = []
    answer = []
    # 取出所有问题
    for i in json.loads(test.questions):
        question = Question.objects.get(id=i)
        # 问题的选项列表
        tmp_choice = json.loads(question.choice)
        tmp_choice_bak = json.loads(question.choice)
        # 对原选项进行乱序
        random.shuffle(tmp_choice)
        # 一个新的列表，存放新选项在旧选项中对应的位置
        tmp_choice_index = []
        for a in tmp_choice:
            tmp_choice_index.append(tmp_choice_bak.index(a))
        choice.append(tmp_choice_index)
        # [1,2,3,4] 答案为4 ,乱序后 [4,2,3,1] 乱序后的编号 [3,1,2,0] 旧的答案编号是3,现在答案编号为0,所以在tmp_choice_index中找旧的答案编号的定位即可
        answer.append(tmp_choice_index.index(question.answer))
    StudentTest.objects.create(test=test, student=student, choice=json.dumps(choice), answer=json.dumps(answer))

@receiver(post_save, sender=Test)
def create_st1(sender, instance=None, created=False, **kwargs):
    if created:
        for student in Student.objects.all():
            create_st(student=student, test=instance)

@receiver(post_save, sender=Student)
def create_st1(sender, instance=None, created=False, **kwargs):
    if created:
        for test in Test.objects.all():
            create_st(student=instance, test=test)
