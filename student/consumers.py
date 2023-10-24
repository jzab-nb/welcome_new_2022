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
