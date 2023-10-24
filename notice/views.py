from django.shortcuts import render
from django.http import HttpResponse

from new.settings import SECRET_KEY

from .models import HeadPhoto, Student, Notice, NoticeStudent
import json, jwt

def json_response(dic):
    return HttpResponse(json.dumps(dic), content_type='json', status=200)

def error_response(msg):
    return HttpResponse(json.dumps({'msg': msg}), content_type='json', status=400)

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')['data']['uuid']

def lbt(request):

    """
    轮播图的函数,返回轮播图的url组成的列表
    """
    list1 = []
    query = HeadPhoto.objects.all()
    for a in query:
        list1.append(a.image.name)
    return json_response(list1)

def notice(request):

    """
    通知的视图函数
    get: 获取当前用户的通知
    post: 增加通知(管理员)
    """
    if request.method == 'GET':
        token = request.headers.get('token')
        list1 = []
        if token:
            uuid = decode_token(token)
            student = Student.objects.get(uuid=uuid)
            for nss in student.noticestudent_set.all():
                list1.append(
                    {
                        "id": nss.id.__str__(),
                        "title": nss.notice.title,
                        "content": nss.notice.content,
                        "read": nss.read,
                        "time": nss.notice.time.__str__(),
                        "img": nss.notice.img(),
                        "author": nss.notice.author
                    }
                )
        else:
            for n in Notice.objects.filter(radio=True):
                list1.append(
                    {
                        "title": n.title,
                        "content": n.content,
                        "time": n.time.__str__(),
                        "img": n.img(),
                        "author": n.author
                    }
                )
        return json_response(list1)
    else:
        return error_response('不被允许的method')

def read(request):
    if request.method == 'POST':
        if request.body:
            nss_id = json.loads(request.body).get('id')
            if nss_id:
                uuid = decode_token(request.headers['token'])
                return json_response(
                    {'count': NoticeStudent.objects.filter(id=nss_id, student_id=uuid).update(read=True)}
                )
        return error_response('参数不全')
    else:
        return error_response("不被允许的method")
