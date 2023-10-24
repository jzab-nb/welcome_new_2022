from django.shortcuts import render
from django.http import HttpResponse
from new.settings import SECRET_KEY
from student.models import Student
from .models import Question

import json, jwt
'''
1.获取所有题目
2.上传答案
'''

def json_response(dic):
    return HttpResponse(json.dumps(dic), content_type='json', status=200)

def error_response(msg):
    return HttpResponse(json.dumps({'msg': msg}), content_type='json', status=400)

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')['data']['uuid']

def is_pass(request):
    uuid = decode_token(request.headers['token'])
    student = Student.objects.get(uuid=uuid)
    sts = student.studenttest_set.all()[0]
    return json_response(sts.is_pass)

def answer(request):
    uuid = decode_token(request.headers['token'])
    student = Student.objects.get(uuid=uuid)
    sts = student.studenttest_set.all()[0]
    if request.method == 'GET':
        lst = []
        choices_change = json.loads(sts.choice)
        questions = json.loads(sts.test.questions)
        for i in range(0, len(questions)):
            question = Question.objects.get(id=questions[i])
            tmp_choice = json.loads(question.choice)
            new_choice = []
            for j in choices_change[i]:
                new_choice.append(tmp_choice[j])
            lst.append(
                {
                    'title': question.title,
                    'choices': new_choice
                }
            )
        return json_response(lst)
    elif request.method == 'POST':
        error = []
        body = json.loads(request.body)
        answers = json.loads(sts.answer)
        if len(answers) != len(body):
            return error_response('答案数组长度不正确')
        for i in range(0, len(answers)):
            if body[i] != answers[i]:
                error.append(i)
        if len(error) == 0:
            sts.is_pass = True
            sts.save()
        dic = {
            'count': len(error),
            'error': error
        }
        return json_response(dic)
    else:
        return error_response('不被允许的请求')
