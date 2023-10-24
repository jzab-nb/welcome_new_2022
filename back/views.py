from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count

from .models import Account
from student.models import Student, ReportInfo, Image
from notice.models import NoticeStudent, Notice, HeadPhoto


import json, os

SEND = []

# BASEURL = 'http://127.0.0.1:8080/'
BASEURL = 'https://vip.jzab.xyz/'

def api(request):
    return HttpResponse(json.dumps(True), content_type='json')

def login(request):
    if request.session.get('username'):
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            account = Account.objects.filter(username=username, password=password)
            if account:
                request.session['username'] = username
                return HttpResponseRedirect('/')
        return render(request, 'login.html', {'msg': '错误'})

def index(request):
    if request.session.get('username') is None:
        return HttpResponseRedirect('/login')
    students = Student.objects.filter(status=0)
    if request.method == 'POST':
        choice = request.POST['choice']
        text = request.POST['text']
        query = students
        if choice == '0':
            query = query.filter(info__name__contains=text)
        elif choice == '1':
            query = query.filter(info__id_card__contains=text)
        elif choice == '2':
            query = query.filter(info__phone_number__contains=text)
        elif choice == '3':
            query = query.filter(info__qq__contains=text)
        students = query
    if students:
        student = students[0]
        image = student.image
        baseurl = BASEURL
        dic = {
            'uuid': student.uuid,
            'number': Student.objects.filter(status=0).aggregate(number=Count('uuid'))['number'],
            'name': student.info.name,
            'id_card': student.info.id_card,
            'phone': student.info.phone_number,
            'qq': student.info.qq,
            'hs': baseurl+image.hs.name,
            'day14': baseurl+image.day14.name,
            'photo': baseurl+image.photo.name,
            'healthy_code': baseurl+image.health_code.name,
            'tour_code': baseurl+image.tour_code.name
        }
    else:
        dic = {'number': students.aggregate(number=Count('uuid'))['number']}
    return render(request, 'index.html', dic)

def check(request):
    dic = json.loads(request.body)
    student = Student.objects.get(uuid=dic['uuid'])
    if student.status != 0:
        return HttpResponse('/')
    choice = dic['choice']
    title = '审核进度通知'
    content = ''
    # 通过
    if choice == 0:
        student.status = 1
        content = student.info.name+' 同学您好,您的防疫照片与信息均已审核通过,望周知'
    # 驳回图片
    if choice == 1:
        student.status = -1
        remove_image(student.image)
        content = student.info.name + ' 同学您好,您的防疫照片有错误的地方,请及时重新上传,有疑问可联系信工科协(QQ群：801314487)'
    # 驳回信息
    if choice == 2:
        student.status = -1
        student.info.delete()
        student.have_info = False
        content = student.info.name + ' 同学您好,您的个人信息有错误的地方,请及时重新上传,有疑问可联系信工科协(QQ群：801314487)'
    # 全部驳回
    if choice == 3:
        student.status = -1
        student.info.delete()
        student.have_info = False
        remove_image(student.image)
        content = student.info.name + ' 同学您好,您的防疫照片与个人信息均有错误的地方,请及时重新上传,有疑问可联系信工科协(QQ群：801314487)'
    new_notice = Notice.objects.create(title=title, content=content, radio=False)
    NoticeStudent.objects.create(student=student, notice=new_notice)
    student.save()
    return HttpResponse('/')

def check_in(request):
    list1 = []
    STATUS = {
        0: '待审核',
        -1: '已驳回',
        2: '未准备',
        1: '已通过'
    }
    if request.method == 'GET':
        query = Student.objects.filter(have_info=True, check_in=False)[:10]
    else:
        query = Student.objects.filter(have_info=True, check_in=False)
        text = request.POST['text']
        choice = request.POST['choice']
        if choice == '0':
            query = query.filter(info__name__contains=text)
        elif choice == '1':
            query = query.filter(info__id_card__contains=text)
        elif choice == '2':
            query = query.filter(info__phone_number__contains=text)
        elif choice == '3':
            query = query.filter(info__qq__contains=text)
    for e in query:
        list1.append({
            'uuid': e.uuid,
            'name': e.info.name,
            'id_card': e.info.id_card,
            'phone': e.info.phone_number,
            'qq': e.info.qq,
            'status': STATUS[e.status],
            'status_id': e.status,
            'head_url': BASEURL + e.image.photo.name
        })
    dic = {
        'list': list1
    }
    return render(request, 'check_in.html', dic)

def lbt(request):
    if request.method == "DELETE":
        print(request.body)
        uuid = json.loads(request.body)['uuid']
        photo = HeadPhoto.objects.get(id=uuid)
        os.remove(photo.image.path)
        photo.delete()
        return HttpResponse('/lbt')
    elif request.method == 'POST':
        print(request.FILES)
        # print(request.body)
        HeadPhoto.objects.create(image=request.FILES['file'])
    list1 = []
    for i in HeadPhoto.objects.all():
        list1.append({
            'url': BASEURL+i.image.name,
            'uuid': i.id
        })
    dic = {
        'list': list1
    }
    return render(request, 'lbt.html', dic)

def notice(request):
    if request.method == 'POST':
        Notice.objects.create(title=request.POST['title'], content=request.POST['content'])
    elif request.method == 'DELETE':
        if json.loads(request.body).get('super'):
            Notice.objects.filter(radio=False, noticestudent__read=True).delete()
            return HttpResponse('/noticemanger')
        uuid = json.loads(request.body)['uuid']
        print(uuid)
        Notice.objects.filter(id=uuid).delete()
        return HttpResponse('/noticemanger')
    dic = {
        'list': Notice.objects.filter(radio=True)
    }
    return render(request, 'notice.html', dic)

def report(request):
    uuid = json.loads(request.body)['uuid']
    student = Student.objects.get(uuid=uuid)
    student.check_in = True
    student.save()
    SEND.append({
        'name': student.info.name,
        'rank': Student.objects.filter(check_in=True).aggregate(rank=Count('uuid'))['rank']
    })
    return HttpResponse('/check_in')

def show(request):
    if len(SEND) == 0:
        return HttpResponse(json.dumps({'msg': '没有新的学生报到'}), status=404, content_type='json')
    return HttpResponse(json.dumps(SEND.pop(0)), content_type='json')

def remove_image(image):
    os.remove(image.hs.path)
    os.remove(image.day14.path)
    os.remove(image.health_code.path)
    os.remove(image.tour_code.path)
    image.hs = Image.DEFAULT
    image.day14 = Image.DEFAULT
    image.health_code = Image.DEFAULT
    image.tour_code = Image.DEFAULT
    image.number = 0
    image.save()
