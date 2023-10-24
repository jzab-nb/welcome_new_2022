# 项目简介

本项目为2022年所使用的新生入学信息采集+欢迎系统的后台,使用django框架开发

前端为微信小程序"信工在线答",还有使用vue开发的大屏幕端.

大屏幕端和后端通信使用websocket协议

后端部署使用uwsgi+nginx的方式

# api文档

base_url = "https://vip.jzab.xyz/"



## 账号与信息采集应用

new/

| url              | method | 请求体                                                   | 响应体                                                       | 备注                                            |
| :--------------- | ------ | -------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------- |
| image/           | get    |                                                          | {'图片名':'图片url'}                                         | 获取所有上传的图片的url                         |
| image/           | post   | {'图片名':图片文件}                                      | {'图片名':'图片url'}                                         | 上传图片文件，可以通过请求体里面的key来动态选择 |
| image/           | delete | ['图片名']                                               | {'图片名':'图片url'}                                         | 删除列表中的对应图片                            |
| student/         | post   | {code: '微信code', name: '姓名',student_number: '学号' } | 成功_200:{     'token': 'token串',     'bound': True/False } 失败_400: {     'msg': '错误信息' } | 绑定身份信息与微信                              |
| student/login    | post   | {code: '微信code' }                                      | 成功_200:{     'msg': '',     'token': '',     'bound': True/False } # 当bound为False时代表未绑定，这时候无法拿到token，需要去绑定 失败_400: {     'msg': '错误信息' } | 微信登录                                        |
| student/         | get    |                                                          | {     'have_info': 是否有信息,     'have_report_info': 是否有报道信息,     'img_number': 已经上传图片的数量,     'have_photo': 是否上传头像,     'name': 学生姓名,     'student_number': 学号,     'status': 当前状态 } | 获取账号的基本信息                              |
| student/check_in | post   | {code:'二维码code'}                                      | {'msg': '信息'}                                              | 通过扫码报道，信息会发往redis                   |
| ...              | ...    | ...                                                      | ...                                                          | ...                                             |

## 通知应用

notice/

| url         | method | 请求体                             | 响应体                                                       | 备注                          |
| ----------- | ------ | ---------------------------------- | ------------------------------------------------------------ | ----------------------------- |
| notice/     | post   | {'title':'标题','content': ''正文} |                                                              | 上传通知                      |
| notice/     | get    |                                    | {'title':'标题','content':'正文','read':'是否已读','id':'唯一id'} | 响应为一个列表，获取通知      |
| notice/lbt  | get    |                                    | ['url1','url2']                                              | 获取轮播图url                 |
| notice/read | post   | {'id': '之前获取到的唯一id'}       | {'count': 1}                                                 | 结果为1是正确的，学生阅读接口 |

## 答题应用

answer/

此部分未使用

## 后台管理

/

此部分为前后端不分离的

## 大屏幕信息传递

ws/

```python
{
    'photo': 照片url,
    'sex': 性别,
    'name': 姓名,
    'province': 省份,
    'city': 城市,
    'rank': 报道名次
}
```

# 项目部署

## 1.生成依赖文件

​	在开发环境下生成requirements.txt文件(若使用虚拟环境，需在虚拟环境内操作)

```
pip freeze > requirements.txt
```

## 2.文件上传服务器

​	项目文件全部上传服务器，但虚拟环境不要上传，因为虚拟环境过于庞大，且不同系统版本虚拟环境格式不一致

## 3.重新创建虚拟环境

​	进入服务器环境，重新生成虚拟环境

```
# 生成虚拟环境
python -m venv venv
# 启用虚拟环境
source venv/bin/activate
# 升级pip安装依赖文件
pip install --upgrade pip
pip install -r requirements.txt
```

## 4.配置并运行uwsgi

在项目同名目录下配置uwsgi.ini文件

```
# 在该文件中，使用';'来注释一行
=====uwsgi.ini=====
[uwsgi]
;第一个配置项为ip和端口，前写http或socket，指明不同的启动方式，后面ip写127.0.0.1为本地，不写或写0或0.0.0.0则广播到网络
http=:8000
;socket=127.0.0.1:8000
;chdir指定项目地址
chdir=/home/xgkx/django/new
;uwsgi-file指定wsgi的python文件的地址，路径是从项目路径开始的相对路径
wsgi-file=new/wsgi.py
;进程数和线程数
process=2
threads=2
;指定pid文件的名称
pidfile=uwsgi.pid
;是否后台启动同时指明日志文件的名称
daemonize=uwsgi.log
;开启主进程管理模式
master=true
```

安装uwsgi

```
pip install uwsgi
```

启动和停止uwsgi

```
uwsgi --ini uwsgi.ini
uwsgi --stop uwsgi.pid
```

## 5.配置nginx

安装nginx

```
apt-get install nginx
```

填写配置文件 /etc/nginx/sites-enabled/default

```
server {
	# 端口
    listen 80;
    listen [::]:80;
    server_name example.com;
    root /var/www/example.com;
    index index.html;
    # 转发
    location / {
        # try_files $uri $uri/ =404;
        # 转发的ip和端口
        uwsgi_pass 127.0.0.1:8080;
        # 导入一些参数，默认的
        include /etc/nginx/uwsgi_params;
    }
}
```

启动nginx

```
sudo /etc/init.d/nginx start   # 启动
sudo /etc/init.d/nginx stop    # 停止
sudo /etc/init.d/nginx restart # 重启
```

## 6.静态文件配置

创建静态文件夹 /static (最内层必须为static)

在settings.py中新增STATIC_ROOT = 静态文件绝对路径

执行manage.py collectstatic

配置nginx

```
location /static {
	root /home/jzab/python/test03;
}
```

# 思路

报道流程: 学生来->工作人员在网页上输入学号->学生报道成功->大屏幕更新学生姓名,并播报欢迎语音

前端: 提前生成每一个学生的欢迎语音,用websocket协议等待后端发送数据,收到数据后(包含学号或者姓名),查找语音文件并播放

后端: 输入框接收学号,提交后更改学生状态为已报道,同时数据传入redis,websocket的进程循环读取redis,有数据则通过websocket进程发送给前端

大屏幕 ----- django

```python
// 后端接口代码片段
import redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)

student.check_in = True
student.check_in_time = datetime.datetime.now()
student.save()
# r.rpush('key', 'value') 右端插入元素
# r.lpop('key') 左端弹出元素
# r.llen('key') 返回长度

dic = json.loads(student.send_info)

r.rpush('send_list', json.dumps(dic))
return Response({'msg': '扫码成功'})

// 后端websocket代码
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
import datetime, threading, redis, json

r = redis.Redis(host='127.0.0.1', port=6379, db=0)


CONNECT = []

def run():
    # print(datetime.datetime.now())
    if r.llen('send_list'):
        text = str(r.lpop('send_list'), encoding='UTF-8')
        print(CONNECT)
        print(text)
        for i in CONNECT:
            i.send(text)
    timer = threading.Timer(5, run)
    timer.start()


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        self.accept()
        if not CONNECT:
            t1 = threading.Timer(1, function=run)
            t1.start()
        CONNECT.append(self)
        print(CONNECT)

    def websocket_receive(self, message):
        print(message)
        self.send(json.dumps({'msg': '回复'}))

    def websocket_disconnect(self, message):
        CONNECT.remove(self)
        raise StopConsumer()
```

