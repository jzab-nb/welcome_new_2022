from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import rest_framework.status as status
from django.db.models import Count

from .models import Info, Student, ReportInfo, Image
from .serializers import InfoSerializers, StudentSerializers
from new.settings import SECRET_KEY

import jwt, datetime, json, os, requests

def excel():
    import xlrd
    # Student.objects.all().delete()
    if not Student.objects.all():
        sheet = xlrd.open_workbook_xls("信息工程学院.xls").sheet_by_index(0)

        print(sheet.nrows)
        for i in range(1, sheet.nrows):
            # print(sheet.cell_value(i, 7)+"_"+sheet.cell_value(i, 19))
            print(sheet.cell_value(i, 20))
            if not sheet.cell_value(i, 20):
                city = ''
            else:
                province = str.split(sheet.cell_value(i, 20), '省')
                if len(province) == 1:
                    city = str.split(sheet.cell_value(i, 20), '市')[0]+'市'
                else:
                    city = str.split(str.split(sheet.cell_value(i, 20), '省')[1], '市')[0]+'市'
                if '定安县' in sheet.cell_value(i, 20):
                    city = '定安县'
                if '巴音郭楞蒙古自治州' in sheet.cell_value(i, 20):
                    city = '巴音郭楞蒙古自治州'
                if '海南藏族自治州' in sheet.cell_value(i, 20):
                    city = '海南藏族自治州'
                if '海西蒙古族藏族自治州' in sheet.cell_value(i, 20):
                    city = '海西蒙古族藏族自治州'
            print(city)
            dic = {
                'photo': '/static/new/photo/'+f'{sheet.cell_value(i, 7)}_{sheet.cell_value(i, 25)}.jpg',
                'sex': sheet.cell_value(i, 9),
                'name': sheet.cell_value(i, 7),
                'province': sheet.cell_value(i, 2),
                'city': city,
                'rank': -1
            }
            Student.objects.create(
                name=sheet.cell_value(i, 7),
                id_card=sheet.cell_value(i, 19),
                student_number=sheet.cell_value(i, 25),
                send_info=json.dumps(dic)
            )
            print(i)


# excel()

class R:
    @staticmethod
    def json_response(dic):
        return HttpResponse(json.dumps(dic), content_type='json')

    @staticmethod
    def disable():
        return Response(
            {'msg': '不被允许的方法'},
            status=status.HTTP_400_BAD_REQUEST
        )

def get_openid(code):
    appid = 'wxa7e2a4f5bd031619'
    secret = 'acc083e520ea83cab7afbcd07aba7086'
    openid = json.loads(requests.get(
        f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
    ).content)
    print(openid)
    openid = openid.get('openid')
    return openid

def create_token(uuid):
    dic = {
        'exp': datetime.datetime.now() + datetime.timedelta(days=5),  # 过期时间
        'iat': datetime.datetime.now(),  # 开始时间
        'iss': 'jzab',  # 签名
        'data': {
            'uuid': uuid
        }
    }
    return jwt.encode(dic, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')['data']['uuid']

def check(student):
    if student.have_info and student.have_report_info and student.image.number == 4:
        student.status = 0
    else:
        student.status = 2
    student.save()

def image(request):

    """
    上传图片
    url: new/image/
    method: post, get, delete
    request:
        post: {
            'photo': 文件.jpg
        }
        delete: ['photo', 'hs', 'health_code', 'tour_code']
    response: {
        "photo": "static/new/photo/孙后才.png"
    }
    备注: post和get获得的响应内容是一样的, 只有post需要带图片文件, 多次请求该接口会覆盖原文件
    """

    uuid = decode_token(request.headers['token'])
    imageSet = Image.objects.get(student_id=uuid)
    student = imageSet.student
    if request.method == 'POST':
        body = request.FILES
        print(body)

        if body.get('hs') is not None:
            imageSet.number += 1
            if Image.DEFAULT != imageSet.hs.name:
                imageSet.number -= 1
                os.remove(imageSet.hs.path)
            imageSet.hs = body['hs']

        if body.get('health_code') is not None:
            imageSet.number += 1
            if Image.DEFAULT != imageSet.health_code.name:
                imageSet.number -= 1
                os.remove(imageSet.health_code.path)
            imageSet.health_code = body['health_code']

        if body.get('tour_code') is not None:
            imageSet.number += 1
            if Image.DEFAULT != imageSet.tour_code.name:
                imageSet.number -= 1
                os.remove(imageSet.tour_code.path)
            imageSet.tour_code = body['tour_code']

        if body.get('photo') is not None:
            imageSet.number += 1
            if Image.DEFAULT != imageSet.photo.name:
                imageSet.number -= 1
                os.remove(imageSet.photo.path)
            imageSet.photo = body['photo']

        imageSet.save()
    elif request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        if request.body:
            body = json.loads(request.body)
        else:
            body = []
        if 'hs' in body and imageSet.hs.name != Image.DEFAULT:
            os.remove(imageSet.hs.path)
            imageSet.hs = Image.DEFAULT
            imageSet.number -= 1
        if 'health_code' in body and imageSet.health_code.name != Image.DEFAULT:
            os.remove(imageSet.health_code.path)
            imageSet.health_code = Image.DEFAULT
            imageSet.number -= 1
        if 'tour_code' in body and imageSet.tour_code.name != Image.DEFAULT:
            os.remove(imageSet.tour_code.path)
            imageSet.tour_code = Image.DEFAULT
            imageSet.number -= 1
        if 'photo' in body and imageSet.photo.name != Image.DEFAULT:
            os.remove(imageSet.photo.path)
            imageSet.photo = Image.DEFAULT
            imageSet.number -= 1
        imageSet.save()
    else:
        return R.json_response({'msg': '不被允许的请求'})
    check(student)
    dic = {
        'hs': imageSet.hs.name,
        'tour_code': imageSet.tour_code.name,
        'health_code': imageSet.health_code.name,
        'photo': imageSet.photo.name,
        'number': imageSet.number
    }
    return R.json_response(dic)


class ReportInfoViewSet(viewsets.ModelViewSet):
    queryset = ReportInfo.objects.all()
    serializer_class = None

    def list(self, request, *args, **kwargs):
        uuid = decode_token(request.headers['token'])
        student = Student.objects.get(uuid=uuid)
        if not student.have_report_info:
            return Response({'msg': '没有信息'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(student.reportinfo.to_dic())

    def create(self, request, *args, **kwargs):
        uuid = decode_token(request.headers['token'])
        student = Student.objects.get(uuid=uuid)
        data = request.data
        info = ReportInfo()
        info.estimated_arrival_time = data.get('estimated_arrival_time')
        info.whether_delay_report = data.get('whether_delay_report')
        info.delay_report_reason = data.get('delay_report_reason')
        info.transportation = data.get('transportation')
        info.car_no = data.get('car_no')
        info.student = student
        student.have_report_info = True
        info.save()
        student.save()
        check(student)
        return Response(info.to_dic())

    def retrieve(self, request, *args, **kwargs):
        return R.disable()

    def update(self, request, *args, **kwargs):
        return R.disable()

    def partial_update(self, request, *args, **kwargs):
        return R.disable()

    def destroy(self, request, *args, **kwargs):
        uuid = decode_token(request.headers['token'])
        student = Student.objects.get(uuid=uuid)
        if not student.have_report_info:
            return Response({'msg': '没有信息'}, status=status.HTTP_404_NOT_FOUND)
        else:
            student.reportinfo.delete()
            student.have_report_info = False
            student.save()
            return Response({'msg': '已删除'})

class InfoViewSet(viewsets.ModelViewSet):
    """
    list:
    查询个人信息列表

    create:
    创建个人信息

    retrieve:
    查询个人信息详情

    update:
    更新个人信息

    partial_update:
    更新个人信息部分属性

    destroy:
    删除个人信息

    """
    queryset = Info.objects.all()
    serializer_class = InfoSerializers

    @staticmethod
    def data_replay(data, uuid):
        TF = {
            '是': True,
            '否': False
        }
        student = Student.objects.get(uuid=uuid)
        data['student'] = uuid
        data['ethnic'] = Info.ETHNIC_CHOICE[int(data['nation']) - 1][0]
        data['political_landscape'] = data['political']
        data['the_religion'] = TF[data['religion']]
        data['religion'] = data['religionname']
        data['phone_number'] = data['phone']
        data['father_name'] = data['fathername']
        data['mother_name'] = data['mothername']
        data['father_phone'] = data['fatherphone']
        data['mother_phone'] = data['motherphone']
        data['detailed_address'] = data['home']
        data['household_address'] = data['idhome']
        data['native_place'] = data['native'][0] + ' ' + data['native'][1] + ' ' + data['native'][2]
        data['origin'] = data['origin'][0] + ' ' + data['origin'][1] + ' ' + data['origin'][2]
        data['name'] = student.name
        data['id_card'] = student.id_card
        data['student_number'] = student.student_number

    def create(self, request, *args, **kwargs):
        """
            上传信息(除了图片)
            url: new/info/
            method: post
            request: {
                "fathername": "想",
                "fatherphone": "13615605359",
                "home": "的",
                "idhome": "的",
                "mothername": "",
                "motherphone": "",
                "nation": "1",
                "native": ["北京市", "北京市", "东城区"],
                "origin": ["北京市", "北京市", "东城区"],
                "phone": "13615605359",
                "political": "共青团员",
                "postcode": "111111",
                "qq": "136156053591",
                "religion": "否",
                "religionname": "",
                "sex": "男",
                "wechat": ""
            }
            response: {
                "student_id": "650ac7b3-a76e-4208-8462-f6dd27ce9448",
                "student": "650ac7b3-a76e-4208-8462-f6dd27ce9448",
                "student_number": "1970717299",
                "id_card": "342601200209266519",
                "name": "肖俊男",
                "sex": "男",
                "ethnic": "汉族",
                "the_religion": false,
                "religion": "",
                "origin": "北京市 北京市 东城区",
                "postcode": "111111",
                "phone_number": "13615605359",
                "political_landscape": "共青团员",
                "father_name": "想",
                "mother_name": "",
                "father_phone": "13615605359",
                "mother_phone": "",
                "detailed_address": "的",
                "native_place": "北京市 北京市 东城区",
                "household_address": "的",
                "qq": "136156053591",
                "wechat": ""
            }
        """
        uuid = decode_token(request.headers['token'])
        data = request.data
        if Student.objects.filter(uuid=uuid):
            student = Student.objects.get(uuid=uuid)
            if student.have_info:
                return Response(InfoSerializers(Info.objects.get(student_id=uuid)).data, status=status.HTTP_200_OK)
            self.data_replay(request.data, uuid)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            student.have_info = True
            # headers = self.get_success_headers(serializer.data)
            serializers = InfoSerializers(Info.objects.get(student_id=uuid))
            data = serializers.data
            data['ethnic'] = Info.ETHNIC_CHOICE.index((data['ethnic'], data['ethnic']))+1
            data['origin'] = data['origin'].split(' ')
            data['native_place'] = data['native_place'].split(' ')
            student.save()
            check(student)
            return Response(data)
        else:
            return Response('error')

    def list(self, request, *args, **kwargs):
        """
        获取信息
        url: new/info/
        method: get
        request: 无
        response:
            成功_200: {
                "student_id": "650ac7b3-a76e-4208-8462-f6dd27ce9448",
                "student": "650ac7b3-a76e-4208-8462-f6dd27ce9448",
                "id_card": "342601200209266519",
                "student_number": "420109070116",
                "name": "肖俊男",
                "sex": "男",
                "ethnic": "汉族",
                "the_religion": false,
                "religion": "",
                "origin": "北京市 北京市 东城区",
                "postcode": "111111",
                "phone_number": "13615605359",
                "political_landscape": "共青团员",
                "father_name": "想",
                "mother_name": "",
                "father_phone": "13615605359",
                "mother_phone": "",
                "detailed_address": "的",
                "native_place": "北京市 北京市 东城区",
                "household_address": "的",
                "qq": "136156053591",
                "wechat": ""
            }
            失败_404: {
                'msg': '没有信息'
            }
        """
        uuid = decode_token(request.headers['token'])
        if Student.objects.get(uuid=uuid).have_info:
            serializers = InfoSerializers(Info.objects.get(student_id=uuid))
            data = serializers.data
            data['ethnic'] = Info.ETHNIC_CHOICE.index((data['ethnic'], data['ethnic']))+1
            data['origin'] = data['origin'].split(' ')
            data['native_place'] = data['native_place'].split(' ')
            return Response(data)
        else:
            return Response({'msg': '没有信息'}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        uuid = decode_token(request.headers['token'])
        if Student.objects.get(uuid=uuid).have_info:
            serializers = InfoSerializers(Info.objects.get(student_id=uuid))
            data = json.loads(serializers.data)
            data['ethnic'] = Info.ETHNIC_CHOICE.index((data['ethnic'], data['ethnic'])) + 1
            data['origin'] = data['origin'].split(' ')
            data['native_place'] = data['native_place'].split(' ')
            return Response(json.dumps(data))
        else:
            return Response({'msg': '没有信息'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return R.disable()

    def partial_update(self, request, *args, **kwargs):
        return R.disable()

    def destroy(self, request, *args, **kwargs):
        """
        删除信息
        url: /new/info/<?>/
        method: delete
        request: 无
        response:
            成功_200: {
                'msg': '已删除'
            }
            失败_404: {
                'msg': '没有信息'
            }
        备注:  url中的<?>可以写成任何值 例如: /new/info/1/
        """
        uuid = decode_token(request.headers['token'])
        student = Student.objects.get(uuid=uuid)
        if student.have_info:
            student.info.delete()
            student.have_info = False
            student.save()
            check(student)
            return Response({'msg': '已删除'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': '没有信息'}, status=status.HTTP_404_NOT_FOUND)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializers

    @action(detail=False, methods=['post', 'get'])
    def check_in(self, request):
        uuid = decode_token(request.headers['token'])
        student = Student.objects.get(uuid=uuid)
        if request.method == 'POST':
            # from .consumers import CONNECT
            import redis
            r = redis.Redis(host='127.0.0.1', port=6379, db=0)
            code = request.data.get('code')
            if code == SECRET_KEY:
                #if student.check_in:
                #    return Response({'msg': '您已经报道'})
                student.check_in = True
                student.check_in_time = datetime.datetime.now()
                student.save()
                # r.rpush('key', 'value') 右端插入元素
                # r.lpop('key') 左端弹出元素
                # r.llen('key') 返回长度
                dic = json.loads(student.send_info)
                dic['rank'] = Student.objects.filter(check_in=True).aggregate(rank=Count('uuid'))['rank']
                r.rpush('send_list', json.dumps(dic))
                # for i in CONNECT:
                #     i.send(student.name)
                return Response({'msg': '扫码成功'})
            else:
                return Response({'msg': '扫码错误'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'GET':
            return Response(student.check_in)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        微信登录
        url: /new/student/login/
        method: post
        request: {
            code: '微信code'
        }
        response:
            成功_200:{
                'msg': '',
                'token': '',
                'bound': True/False
            } # 当bound为False时代表未绑定，这时候无法拿到token，需要去绑定
            失败_400: {
                'msg': '错误信息'
            }
        """
        openid = get_openid(request.data.get('code'))
        if openid is None:
            return Response({'msg': 'code错误'}, status=status.HTTP_400_BAD_REQUEST)
        if Student.objects.filter(openid=openid):
            student = Student.objects.get(openid=openid)
            return Response(
                {'token': create_token(student.uuid.__str__()), 'bound': True, 'name': student.name, 'student_number': student.student_number},
                status=status.HTTP_200_OK
            )
        return Response(
            {'msg': '还未绑定身份信息', 'bound': False},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        """
        绑定身份信息与微信
        url: /new/student/
        method: post
        request: {
            code: '微信code',
            name: '姓名',
            student_number: '学号'
        }
        response:
            成功_200:{
                'token': '',
                'bound': True
            }
            失败_400: {
                'msg': '错误信息'
            }
        """
        openid = get_openid(request.data.get('code'))
        if openid is None:
            return Response({'msg': 'code错误'}, status=status.HTTP_400_BAD_REQUEST)
        if Student.objects.filter(openid=openid):
            return Response({'msg': '该微信号已经绑定'}, status=status.HTTP_400_BAD_REQUEST)
        name = request.data.get('name')
        student_number = request.data.get('student_number')
        if name and student_number and Student.objects.filter(student_number=student_number, name=name):
            student = Student.objects.filter(student_number=student_number, name=name)[0]
            if student.openid:
                return Response({'msg': '该学号已经有微信号绑定'}, status=status.HTTP_404_NOT_FOUND)
            student.openid = openid
            student.save()
            return Response(
                {'token': create_token(student.uuid.__str__()), 'bound': True, 'name': student.name, 'student_number': student.student_number},
                status=status.HTTP_200_OK
            )
        else:
            return Response({'msg': '姓名或学号错误'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        uuid = decode_token(request.headers['token'])
        student = Student.objects.get(uuid=uuid)
        dic = {
            'have_info': student.have_info,
            'have_report_info': student.have_report_info,
            'img_number': student.image.number,
            'have_photo': not student.image.photo == Image.DEFAULT,
            'name': student.name,
            'student_number': student.student_number,
            'status': student.status
        }
        return Response(dic, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return R.disable()

    def update(self, request, *args, **kwargs):
        return R.disable()

    def partial_update(self, request, *args, **kwargs):
        return R.disable()

    def destroy(self, request, *args, **kwargs):
        return R.disable()
