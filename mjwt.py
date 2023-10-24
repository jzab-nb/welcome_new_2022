import jwt as j
from new.settings import SECRET_KEY
import datetime

def create_token(uuid):
    dic = {
        'exp': datetime.datetime.now() + datetime.timedelta(days=5),  # 过期时间
        'iat': datetime.datetime.now(),  # 开始时间
        'iss': 'jzab',  # 签名
        'data': {
            'uuid': uuid
        }
    }
    return j.encode(dic, SECRET_KEY, algorithm='HS256')


print(create_token('bb06d643-22d5-4ccd-847d-e4914d10bfdd'))

import xlrd, os

# sheet = xlrd.open_workbook_xls("信息工程学院.xls").sheet_by_index(0)
# print(os.getcwd())
# os.chdir('static/new/photo')
# print(os.getcwd())
# lst=os.listdir()
# for i in range(1, sheet.nrows):
#     name = sheet.cell_value(i, 7)
#     student_number = sheet.cell_value(i, 25)
#     photo = f'{name}_{student_number}.jpg'
#     if photo in lst:
#         lst.remove(photo)
#     else:
#         print(photo)
#         for j in lst:
#             if name in j or student_number in j:
#                 os.rename(j, photo)
#
# print(lst)
